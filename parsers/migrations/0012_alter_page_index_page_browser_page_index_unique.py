# Generated by Django 4.0.4 on 2022-05-08 16:46

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0011_browser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='index',
            field=models.PositiveSmallIntegerField(help_text="position at the browser's page list"),
        ),
        migrations.AddConstraint(
            model_name='page',
            constraint=models.UniqueConstraint(django.db.models.expressions.F('browser'), django.db.models.expressions.F('index'), name='browser_page_index_unique'),
        ),
    ]
