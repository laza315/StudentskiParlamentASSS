# Generated by Django 5.0.1 on 2024-02-03 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anketa', '0005_anketa_broj_kodova_alter_anketa_naziv'),
    ]

    operations = [
        migrations.CreateModel(
            name='VezaPredmeti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VezaProfesori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VezaSmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
