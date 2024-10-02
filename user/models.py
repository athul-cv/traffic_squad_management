from django.db import models
# Create your models here.

class Driver_registration(models.Model):
    license_id=models.CharField(max_length=255)
    driver_email=models.EmailField()
    driver_password=models.CharField(max_length=255)
    driver_name=models.CharField(max_length=255)
    address=models.TextField()
    class_of_vehicle=models.CharField(max_length=255)
    license_issue_date=models.DateField(auto_now=True)
    license_expire_date=models.DateField(auto_now=True)
    registered_at=models.DateField(auto_now_add=True)


class Reporting(models.Model):
    user = models.ForeignKey(Driver_registration, on_delete=models.CASCADE)
    accident_type = models.CharField(max_length=255)
    accident_desc = models.TextField()
    accident_loc = models.CharField(max_length=255)
    accident_date = models.DateField(auto_now=True)
    accident_time = models.TimeField()
    accident_image = models.ImageField(upload_to="report/")