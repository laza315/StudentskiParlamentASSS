# Generated by Django 5.0.1 on 2024-02-08 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anketa', '0011_promena_int'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anketa',
            name='smer',
            field=models.CharField(choices=[('Informatika', 'Informatika'), ('Drumski Saobracaj', 'Drumski Saobracaj'), ('Privredno Inzinjerstvo', 'Privredno Inzinjerstvo')], default='Informatika'),
        ),
    ]
