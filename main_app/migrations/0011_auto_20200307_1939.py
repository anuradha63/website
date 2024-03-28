# Generated by Django 3.0a1 on 2020-03-07 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_heavenuserinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='labuserinfo',
            name='prog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Prog'),
        ),
        migrations.AddField(
            model_name='studentuserinfo',
            name='prog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Prog'),
        ),
    ]
