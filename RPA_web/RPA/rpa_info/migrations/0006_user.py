# Generated by Django 2.2 on 2020-04-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpa_info', '0005_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('passwd', models.CharField(max_length=100)),
            ],
        ),
    ]
