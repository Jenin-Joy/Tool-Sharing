# Generated by Django 5.1.5 on 2025-03-08 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0002_rename_user_location_tbl_user_user_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_user',
            name='user_status',
            field=models.IntegerField(default=0),
        ),
    ]
