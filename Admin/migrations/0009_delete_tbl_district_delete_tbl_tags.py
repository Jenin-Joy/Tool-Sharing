# Generated by Django 5.1.5 on 2025-03-07 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0008_tbl_tags'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tbl_district',
        ),
        migrations.DeleteModel(
            name='tbl_tags',
        ),
    ]
