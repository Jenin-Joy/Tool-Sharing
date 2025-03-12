# Generated by Django 5.1.5 on 2025-03-07 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0016_tbl_tool_tbl_renttool_tbl_rating_tbl_bookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_tool',
            name='gallery',
            field=models.FileField(default='Assets/gallery/default.jpg', upload_to='Assets/gallery/'),
        ),
        migrations.CreateModel(
            name='tbl_gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_file', models.FileField(upload_to='Assets/gallery/')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.tbl_tool')),
            ],
        ),
    ]
