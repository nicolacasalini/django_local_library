# Generated by Django 2.2.5 on 2020-04-12 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='borrower',
        ),
    ]
