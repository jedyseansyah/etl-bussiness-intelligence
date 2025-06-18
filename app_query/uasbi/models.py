from django.db import models

# Create your models here.
class FactCampaign(models.Model):
    product = models.CharField(max_length=255)
    year = models.IntegerField()
    month = models.IntegerField()
    units_sold = models.IntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=3)
    operating_profit = models.DecimalField(max_digits=15, decimal_places=3)
    roi = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.product} - {self.year}/{self.month}"

class FactCustomer(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    product = models.CharField(max_length=255)
    units_sold = models.IntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=3)
    operating_profit = models.DecimalField(max_digits=15, decimal_places=3)

    def __str__(self):
        return f"{self.product} in {self.city}, {self.state} - {self.year}/{self.month}"

class FactSales(models.Model):
    product = models.CharField(max_length=255)
    year = models.IntegerField()
    month = models.IntegerField()
    retailer = models.CharField(max_length=100)
    sales_method = models.CharField(max_length=50)
    units_sold = models.IntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=3)
    operating_profit = models.DecimalField(max_digits=15, decimal_places=3)

    def __str__(self):
        return f"{self.product} by {self.retailer} ({self.sales_method}) - {self.year}/{self.month}"