# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-07 22:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institucion', '0001_initial'),
        ('localizaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denuncia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('denuncia', models.TextField(blank=True)),
                ('referencia', models.CharField(blank=True, default='', max_length=140)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('tipo', models.CharField(choices=[('CR', 'Criminal'), ('MU', 'Municipal'), ('MA', 'Medio Ambiente'), ('DH', 'Derechos Humanos')], default='CR', max_length=2)),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizaciones.Direccion')),
            ],
        ),
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('motivo', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField(default=0)),
                ('tipo', models.CharField(choices=[('CR', 'Criminal'), ('MU', 'Municipal'), ('MA', 'Medio Ambiente'), ('DH', 'Derechos Humanos')], default='CR', max_length=2)),
                ('instituciones', models.ManyToManyField(to='institucion.Institucion')),
            ],
            options={
                'ordering': ['-cantidad'],
                'verbose_name': 'Motivos',
            },
        ),
        migrations.AddField(
            model_name='denuncia',
            name='motivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='denuncia.Motivo'),
        ),
    ]