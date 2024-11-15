from django.db import models


#this table for details of registerpage
class Details(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    date_of_birth=models.DateField()
    account_number=models.IntegerField()
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
#this is table for transfer of transferpage
from django.utils import timezone
class Transaction(models.Model):
    source_account = models.IntegerField()
    transaction_type = models.CharField(max_length=100, default='debit')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
