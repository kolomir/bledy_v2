# Generated by Django 3.1.2 on 2022-12-18 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bledy', '0003_alter_lider_dzial_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bledy',
            name='zakonczony',
            field=models.BooleanField(default=False),
        ),
    ]
