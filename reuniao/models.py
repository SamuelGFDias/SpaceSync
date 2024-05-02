import re
from datetime import timedelta

from django.db import models
from django.core.exceptions import ValidationError


class Membro(models.Model):
    TIPO = [
        ('C', 'Convidado'),
        ('F', 'Funcionário'),
    ]
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    celular = models.CharField(max_length=15)
    tipo = models.CharField(max_length=1, choices=TIPO, null=False, blank=False, default='C')

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        pattern = r'^\(\d{2}\)\s9\d{4}-\d{4}$'
        if not re.match(pattern, self.celular):
            raise ValidationError('Número de celular inválido. O formato correto é (XX) 9XXXX-XXXX.')

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'


class Filial(models.Model):
    descricao = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'


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

        # Verifica se já existe outra reunião na mesma ao mesmo período
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
