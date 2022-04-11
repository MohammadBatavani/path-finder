# Generated by Django 3.1.7 on 2021-07-31 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0002_auto_20210722_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_point', models.JSONField()),
                ('destination_point', models.JSONField()),
                ('res_dir', models.JSONField()),
                ('res_dir_distance', models.FloatField()),
                ('res_2d_distance', models.FloatField()),
                ('res_time_of_arrival', models.FloatField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]