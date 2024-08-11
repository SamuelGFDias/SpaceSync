from django.contrib import admin
from django import forms
from .models import Membro, Filial, Sala, Reuniao


class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = '__all__'
        widgets = {
            'celular': forms.TextInput(attrs={'id': 'id_celular'}),
        }

    class Media:
        js = ('reuniao/static/formatar_telefone.js',)


class MembroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'email', 'celular', 'tipo')
    list_display_links = ('id', 'nome', 'cpf')
    search_fields = ('id', 'nome', 'tipo')
    list_filter = ('tipo',)
    list_per_page = 10


admin.site.register(Membro, MembroAdmin)


class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao')
    list_display_links = ('id', 'descricao')
    search_fields = ('id', 'descricao')
    list_per_page = 10


admin.site.register(Filial, FilialAdmin)


class SalaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'filial')
    list_display_links = ('id', 'descricao')
    search_fields = ('id', 'descricao')
    list_filter = ('filial',)
    list_per_page = 10


admin.site.register(Sala, SalaAdmin)


class ReuniaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'motivo', 'sala', 'hora_inicial', 'hora_final')
    list_display_links = ('id',)
    search_fields = ('id',)
    list_filter = ('sala', 'hora_inicial', 'hora_final')
    list_per_page = 10


admin.site.register(Reuniao, ReuniaoAdmin)
