# Generated by Django 4.0.4 on 2022-05-13 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0023_remove_sitelanguage_parser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='novelparser',
            old_name='icon',
            new_name='logo',
        ),
    ]
