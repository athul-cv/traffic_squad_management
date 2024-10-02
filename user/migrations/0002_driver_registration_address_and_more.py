# Generated by Django 5.0.2 on 2024-03-18 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver_registration',
            name='address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver_registration',
            name='class_of_vehicle',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='driver_registration',
            name='license_expire_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='driver_registration',
            name='license_issue_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='driver_registration',
            name='registered_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]