# Generated by Django 5.1.4 on 2025-01-17 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_remove_map_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
