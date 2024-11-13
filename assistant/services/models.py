from django.db import models

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    manager_id = models.IntegerField()
    service_name = models.CharField(max_length=100)
    description = models.TextField()

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    service_manager_id = models.IntegerField()
    service_id = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100)

class CustomerSchedule(models.Model):
    customer_id = models.IntegerField()
    schedule_id = models.IntegerField()
    confirmed_by_customer = models.IntegerField()
