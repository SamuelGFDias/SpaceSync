from rest_framework import serializers
from reuniao.models import Reuniao, Membro, Sala, Filial


class ReuniaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reuniao
        fields = '__all__'


class MembroSerializer(serializers.ModelSerializer):
    membro_nome = serializers.ReadOnlyField(source='membro.nome')

    class Meta:
        model = Membro
        fields = '__all__'


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'


class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'
