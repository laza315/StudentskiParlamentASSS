# Generated by Django 5.0.1 on 2024-03-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anketa', '0027_alter_vote_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='votes',
            field=models.IntegerField(choices=[(1, 'Нисам задовољан'), (2, 'Oнако'), (3, 'Задовољан'), (4, 'Одлично')], default='3'),
        ),
    ]
