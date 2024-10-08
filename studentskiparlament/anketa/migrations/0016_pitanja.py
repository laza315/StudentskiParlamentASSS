# Generated by Django 4.1.5 on 2024-02-16 12:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anketa', '0015_izmenasmera'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pitanja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('redni_broj', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('anketa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='anketa.anketa')),
            ],
        ),
    ]
