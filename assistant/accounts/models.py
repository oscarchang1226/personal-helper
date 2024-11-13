from django.db import models

class ServiceManager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, null=True)
    email = models.EmailField()

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=100)
    account_status = models.CharField(max_length=100)
    service_manager = models.ForeignKey(ServiceManager, on_delete=models.CASCADE)

class CustomerAccount(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    payment_flag = models.BooleanField()

