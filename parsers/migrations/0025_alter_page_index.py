# Generated by Django 4.0.4 on 2022-05-26 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0024_rename_icon_novelparser_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='index',
            field=models.CharField(help_text='page index from the browser', max_length=100),
        ),
    ]