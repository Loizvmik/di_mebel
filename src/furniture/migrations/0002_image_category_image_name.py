# Generated by Django 5.1.6 on 2025-02-15 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furniture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
