# Generated by Django 4.0.4 on 2022-05-08 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0009_sitelanguage_flag_sitelanguage_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='blocks',
        ),
        migrations.AddField(
            model_name='block',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parsers.resource'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]