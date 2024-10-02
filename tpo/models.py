from django.db import models

# Create your models here.


class IssueFine(models.Model):
    ref_no = models.IntegerField()
    police_id = models.CharField(max_length=20)
    license_id = models.CharField(max_length=20)
    vehicle_no = models.CharField(max_length=20)
    class_of_vehicle = models.CharField(max_length=20)
    place = models.CharField(max_length=255)
    issued_date = models.DateField(auto_now_add=True)
    issued_time = models.TimeField()
    expired_date = models.DateField(auto_now=True)
    court_date = models.DateField(auto_now=True)
    provision = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=25, default="pending")
    paid_date = models.DateField(null=True)

