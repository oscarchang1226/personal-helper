from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_value = models.CharField(max_length=100)
    contact_type = models.CharField(max_length=100)
    contact_label = models.CharField(max_length=100)

class CustomerContact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

class Waitlist(models.Model):
    waitlist_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_id = models.IntegerField()
    waitlisted_at = models.DateTimeField()
    status = models.CharField(max_length=100)
