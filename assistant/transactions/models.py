from django.db import models

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    transaction_date = models.DateTimeField()
    customer_id = models.IntegerField()
    account_id = models.IntegerField()
    schedule_id = models.IntegerField()
    transaction_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
