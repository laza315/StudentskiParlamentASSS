# Generated by Django 4.1.5 on 2024-02-21 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anketa', '0020_pitanja_redni_broj_alter_pitanja_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Izbori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=255)),
                ('votes', models.IntegerField(choices=[(1, 'Nisam zadovoljan'), (2, 'Onako'), (3, 'Zadovoljan'), (4, 'Odlično'), (5, 'Uzdržan')], default=3)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anketa.pitanja')),
            ],
        ),
    ]
