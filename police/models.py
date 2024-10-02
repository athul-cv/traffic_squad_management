from django.db import models

# Create your models here.

class Traffic_police(models.Model):
    police_id=models.IntegerField()
    officer_email=models.EmailField()
    officer_password=models.CharField(max_length=255)
    officer_name=models.CharField(max_length=255)
    police_station=models.CharField(max_length=255)
    court=models.CharField(max_length=255)
    registered_at=models.DateField(auto_now=True)

class Fine_tickets(models.Model):
    section_of_act=models.CharField(max_length=255)
    provision=models.CharField(max_length=255)
    fine_amount=models.DecimalField(max_digits=10,decimal_places=2)


