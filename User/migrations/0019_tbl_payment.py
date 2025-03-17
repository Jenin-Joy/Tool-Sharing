# Generated by Django 5.1.7 on 2025-03-17 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0003_tbl_user_user_status'),
        ('User', '0018_remove_tbl_tool_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.CharField(max_length=50)),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('payment_status', models.IntegerField(default=0)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.tbl_renttool')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_user')),
            ],
        ),
    ]
