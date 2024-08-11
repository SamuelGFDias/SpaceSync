import re
from datetime import timedelta

from django.db import models
from django.core.exceptions import ValidationError


def formatar_telefone(value):
    # Remove todos os caracteres não numéricos
    telefone = re.sub(r'\D', '', value)

    # Verifica se o número possui 11 dígitos (para números no formato (XX) 9XXXX-XXXX)
    if len(telefone) == 11:
        return f"({telefone[:2]}) {telefone[2]}{telefone[3:7]}-{telefone[7:]}"
    else:
        raise ValidationError('Número de celular inválido. Deve ter 11 dígitos.')

    return telefone


def validar_cpf(value):
    cpf = re.sub(r'\D', '', value)  # Remove caracteres não numéricos
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos.')

    if cpf in [str(i) * 11 for i in range(10)]:
        raise ValidationError('CPF inválido.')

    # Validação dos dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if str(digito) != cpf[i]:
            raise ValidationError('CPF inválido.')

    # Formata o CPF para o padrão "XXX.XXX.XXX-XX"
    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

    return cpf_formatado


class Membro(models.Model):
    TIPO = [
        ('C', 'Convidado'),
        ('F', 'Funcionário'),
    ]
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, null=False, blank=False, default='000.000.000-00', validators=[validar_cpf])
    email = models.EmailField()
    celular = models.CharField(max_length=15, validators=[formatar_telefone])
    tipo = models.CharField(max_length=1, choices=TIPO, null=False, blank=False, default='C')

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Verifica se já existe uma instância com este CPF no banco de dados
        if self.pk:
            # Obtenha o objeto existente do banco de dados
            old_instance = Membro.objects.get(pk=self.pk)
            # Se o CPF foi alterado, levanta um erro
            if old_instance.cpf != self.cpf:
                raise ValidationError('Alteração do CPF não é permitida.')

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.cpf = validar_cpf(self.cpf)
        self.celular = formatar_telefone(self.celular)

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        unique_together = ('cpf',)


class Filial(models.Model):
    descricao = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'
        unique_together = ('descricao',)


class Sala(models.Model):
    descricao = models.CharField(max_length=100)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'


class Reuniao(models.Model):
    motivo = models.CharField(max_length=100)
    membros = models.ManyToManyField(Membro, blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    hora_inicial = models.DateTimeField()
    hora_final = models.DateTimeField()

    def __str__(self):
        return self.motivo

    def clean(self):
        super().clean()

        # Verifica se hora inicial é menor que hora final
        if self.hora_inicial >= self.hora_final:
            raise ValidationError("A hora inicial deve ser anterior à hora final.")

        # Verifica se a reunião tem pelo menos 30 minutos
        if self.hora_final - self.hora_inicial < timedelta(minutes=30):
            raise ValidationError("A reunião deve ter pelo menos 30 minutos de duração.")

        # Verifica se a reunião não passa de 3 horas
        if self.hora_final - self.hora_inicial > timedelta(hours=3):
            raise ValidationError("A reunião não pode durar mais de 3 horas.")

        # Verifica se já existe outra reunião na mesma sala ao mesmo período
        conflitos = Reuniao.objects.filter(
            hora_inicial__lt=self.hora_final,
            hora_final__gt=self.hora_inicial,
            sala=self.sala
        )
        if self.pk:
            conflitos = conflitos.exclude(pk=self.pk)

        if conflitos.exists():
            primeiro_conflito = conflitos.first()
            conflito_msg = f"Já existe uma reunião agendada para o período: {primeiro_conflito.hora_inicial.strftime('%d/%m/%Y %H:%M')} - {primeiro_conflito.hora_final.strftime('%d/%m/%Y %H:%M')} na sala {primeiro_conflito.sala}."
            raise ValidationError(conflito_msg)

    class Meta:
        verbose_name = 'Reunião'
        verbose_name_plural = 'Reuniões'
        ordering = ['-hora_final']
