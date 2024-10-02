# Generated by Django 5.0.2 on 2024-03-20 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fine_tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_of_act', models.CharField(max_length=255)),
                ('provisin', models.CharField(max_length=255)),
                ('fine_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]