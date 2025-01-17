# Generated by Django 5.0.2 on 2024-03-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='driver_registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_id', models.CharField(max_length=255)),
                ('driver_email', models.EmailField(max_length=254)),
                ('driver_password', models.CharField(max_length=255)),
                ('driver_name', models.CharField(max_length=255)),
                ('license_issue_date', models.DateField(auto_now_add=True)),
                ('license_expire_date', models.DateField(auto_now_add=True)),
                ('registered_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
