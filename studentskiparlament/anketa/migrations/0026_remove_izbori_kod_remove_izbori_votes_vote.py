# Generated by Django 5.0.1 on 2024-03-07 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anketa', '0025_izbori_kod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='izbori',
            name='kod',
        ),
        migrations.RemoveField(
            model_name='izbori',
            name='votes',
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votes', models.IntegerField(choices=[(1, 'Nisam zadovoljan'), (2, 'Onako'), (3, 'Zadovoljan'), (4, 'Odlično')], default='')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anketa.izbori')),
                ('kod_value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='anketa.backupkod')),
            ],
        ),
    ]
