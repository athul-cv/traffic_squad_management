# Generated by Django 5.0.2 on 2024-03-11 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Traffic_police',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('police_id', models.IntegerField()),
                ('officer_email', models.EmailField(max_length=254)),
                ('officer_password', models.CharField(max_length=255)),
                ('officer_name', models.CharField(max_length=255)),
                ('police_station', models.CharField(max_length=255)),
                ('court', models.CharField(max_length=255)),
                ('registered_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
