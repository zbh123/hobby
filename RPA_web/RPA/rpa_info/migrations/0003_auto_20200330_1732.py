# Generated by Django 2.2 on 2020-03-30 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpa_info', '0002_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='time_person',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='time_rpa',
            field=models.CharField(max_length=50, null=True),
        ),
    ]