from rest_framework import viewsets, generics
from reuniao.models import Reuniao, Membro, Sala, Filial
from reuniao.serializer import ReuniaoSerializer, MembroSerializer, SalaSerializer, FilialSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def view_set(model, serializer):
    queryset = model.objects.all()
    serializer_class = serializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    return queryset, serializer_class, authentication_classes, permission_classes


class ReuniaoViewSet(viewsets.ModelViewSet):
    queryset, serializer_class, authentication_classes, permission_classes = view_set(Reuniao, ReuniaoSerializer)


class MembroViewSet(viewsets.ModelViewSet):
    queryset, serializer_class, authentication_classes, permission_classes = view_set(Membro, MembroSerializer)


class SalaViewSet(viewsets.ModelViewSet):
    queryset, serializer_class, authentication_classes, permission_classes = view_set(Sala, SalaSerializer)


class FilialViewSet(viewsets.ModelViewSet):
    queryset, serializer_class, authentication_classes, permission_classes = view_set(Filial, FilialSerializer)

