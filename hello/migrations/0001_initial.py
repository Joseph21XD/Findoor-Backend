# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sitio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
				('latitud',	models.CharField(max_length=15)),
				('longuitud',	models.CharField(max_length=15)),
				('direccion', models.CharField(max_length=50)),
				('descripcion', models.CharField(max_length=50)),
				('imagen', models.CharField(max_length=200)),
            ],
        ),
		migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
				('apellido', models.CharField(max_length=15)),
				('isFacebook', models.IntegerField()),
				('correo',	models.CharField(max_length=30)),
				('contrasenna', models.CharField(max_length=20)),
				('token', models.CharField(max_length=20)),
				('imagen', models.CharField(max_length=200)),
            ],
        ),
		migrations.CreateModel(
            name='Recomendacion',
            fields=[
               ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
				('latitud',	models.CharField(max_length=15)),
				('longuitud',	models.CharField(max_length=15)),
				('direccion', models.CharField(max_length=50)),
				('descripcion', models.CharField(max_length=50)),
				('imagen', models.CharField(max_length=200)),
				('persona',models.ForeignKey(to='Persona', on_delete=models.CASCADE)),
            ],
        ),
		migrations.CreateModel(
            name='Calificacion',
            fields=[
               ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('persona',models.ForeignKey(to='Persona', on_delete=models.CASCADE)),
				('sitio',models.ForeignKey(to='Sitio', on_delete=models.CASCADE)),
				('rate',models.IntegerField(blank=True)),
            ],
        ),
		migrations.CreateModel(
            name='Comentario',
            fields=[
               ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('persona',models.ForeignKey(to='Persona', on_delete=models.CASCADE)),
				('sitio',models.ForeignKey(to='Sitio', on_delete=models.CASCADE)),
				('comentario',models.CharField(max_length=200)),
            ],
        ),
		migrations.CreateModel(
            name='Visitado',
            fields=[
               ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('persona',models.ForeignKey(to='Persona', on_delete=models.CASCADE)),
				('sitio',models.ForeignKey(to='Sitio', on_delete=models.CASCADE)),
            ],
        ),
		migrations.CreateModel(
            name='Favorito',
            fields=[
               ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('persona',models.ForeignKey(to='Persona', on_delete=models.CASCADE)),
				('sitio',models.ForeignKey(to='Sitio', on_delete=models.CASCADE)),
            ],
        ),
		migrations.CreateModel(
            name='Seguidor',
            fields=[
               ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('seguidor',models.ForeignKey(to='Persona', on_delete=models.CASCADE, related_name = "seguidor")),
				('seguido',models.ForeignKey(to='Persona', on_delete=models.CASCADE, related_name = "seguido")),
            ],
        ),
    ]