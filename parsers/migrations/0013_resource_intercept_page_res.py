# Generated by Django 4.0.4 on 2022-05-09 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0012_alter_page_index_page_browser_page_index_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='intercept_page_res',
            field=models.CharField(blank=True, help_text='put the types of resources that should not be loaded through "_". for example: img_css.resource types: css img font fetch media js', max_length=100),
        ),
    ]
