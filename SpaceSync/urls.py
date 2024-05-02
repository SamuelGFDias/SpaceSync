from django.contrib import admin
from django.urls import path, include
from reuniao.views import FilialViewSet, SalaViewSet, MembroViewSet, ReuniaoViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('filiais', FilialViewSet, basename='Filiais')
router.register('salas', SalaViewSet, basename='Salas')
router.register('membros', MembroViewSet, basename='Membros')
router.register('reunioes', ReuniaoViewSet, basename='Reunioes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
