# Generated by Django 5.0.4 on 2024-05-01 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Membro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('celular', models.CharField(max_length=15)),
                ('tipo', models.CharField(choices=[('C', 'Convidado'), ('F', 'Funcionário')], default='C', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reuniao.filial')),
            ],
        ),
        migrations.CreateModel(
            name='Reuniao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(max_length=100)),
                ('hora_inicial', models.DateTimeField()),
                ('hora_final', models.DateTimeField()),
                ('membro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reuniao.membro')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reuniao.sala')),
            ],
        ),
    ]
