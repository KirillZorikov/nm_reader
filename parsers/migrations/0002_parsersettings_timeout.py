# Generated by Django 4.0.4 on 2022-05-02 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parsersettings',
            name='timeout',
            field=models.PositiveSmallIntegerField(default=40, help_text='how many seconds will the tab be running before TimeoutException'),
        ),
    ]
