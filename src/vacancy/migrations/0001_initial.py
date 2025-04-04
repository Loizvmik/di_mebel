# Generated by Django 5.1.6 on 2025-03-29 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='VacancyPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('vacancyId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='form', to='vacancy.vacancy')),
            ],
        ),
    ]
