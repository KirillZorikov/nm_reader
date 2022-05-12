# Generated by Django 4.0.4 on 2022-05-07 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0007_novelparser_browser_alter_novelparser_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('code', models.CharField(help_text='language code', max_length=10)),
                ('is_main', models.BooleanField(default=True)),
                ('parser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsers.parser')),
            ],
            options={
                'verbose_name': 'SiteLanguage',
                'verbose_name_plural': 'SiteLanguages',
            },
        ),
    ]
