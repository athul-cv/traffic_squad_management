from django.db import models
from user.models import Driver_registration
# Create your models here.
class Add_vehicle(models.Model):
    vehicle_no = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=255)
    fuel_type = models.CharField(max_length=255)
    license_id = models.ForeignKey(Driver_registration,on_delete=models.CASCADE)