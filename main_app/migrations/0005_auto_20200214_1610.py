# Generated by Django 3.0a1 on 2020-02-14 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20200214_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='btpuserinfo',
            name='approval_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='labuserinfo',
            name='approval_status',
            field=models.IntegerField(default=0),
        ),
    ]
