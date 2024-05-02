from django.contrib import admin
from .models import Membro, Filial, Sala, Reuniao


class MembroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'celular', 'tipo')
    list_display_links = ('id', 'nome')
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
