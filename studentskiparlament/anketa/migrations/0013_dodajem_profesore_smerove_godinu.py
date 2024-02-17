# Generated by Django 5.0.1 on 2024-02-11 16:12

import django.core.validators
import django.db.models.deletion
import django_enum.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anketa', '0012_vracanjeuchar'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='anketa',
            name='godina',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AddField(
            model_name='anketa',
            name='tip_ankete',
            field=django_enum.fields.EnumPositiveSmallIntegerField(choices=[(1, 'Profesori'), (2, 'Predmeti')], default=1),
        ),
        migrations.AlterField(
            model_name='anketa',
            name='broj_kodova',
            field=models.IntegerField(default=10, validators=[django.core.validators.MaxValueValidator(150), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.CreateModel(
            name='VezaPredmeti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anketa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anketa.anketa')),
                ('predmet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.predmeti')),
            ],
        ),
        migrations.CreateModel(
            name='VezaProfesori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anketa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anketa.anketa')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.profesori')),
            ],
        ),
    ]
