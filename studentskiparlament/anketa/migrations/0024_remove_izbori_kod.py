# Generated by Django 5.0.1 on 2024-03-02 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anketa', '0023_izbori_kod_alter_izbori_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='izbori',
            name='kod',
        ),
    ]
