# Generated by Django 2.0.5 on 2018-05-13 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourmarks', '0002_auto_20180512_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
