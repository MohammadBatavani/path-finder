# Generated by Django 3.1.7 on 2021-09-18 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_algorithm'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='height_meter',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='width_meter',
            field=models.IntegerField(default=200),
            preserve_default=False,
        ),
    ]
