# Generated by Django 4.0.4 on 2022-05-07 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0003_page_fails_count_alter_parser_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='NovelParser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('url', models.CharField(help_text='novel site url', max_length=100)),
                ('name', models.CharField(help_text='novel site name', max_length=100)),
                ('slug', models.SlugField(blank=True, help_text='unique key for url generation', max_length=100)),
                ('icon', models.ImageField(blank=True, help_text='site icon', null=True, upload_to='site_icons/')),
            ],
            options={
                'verbose_name': 'NovelParser',
                'verbose_name_plural': 'NovelParsers',
            },
        ),
        migrations.AlterField(
            model_name='parser',
            name='type',
            field=models.CharField(choices=[('Translate', 'Translate'), ('TranslateImage', 'Translate Image'), ('Novel', 'Novel')], max_length=50),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('urn', models.CharField(help_text='resource page urn', max_length=255)),
                ('name', models.CharField(help_text='resource page name', max_length=100)),
                ('description', models.CharField(blank=True, help_text='novel site name', max_length=255)),
                ('novel_parser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsers.novelparser')),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
            },
        ),
    ]
