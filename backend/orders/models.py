from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    sales = models.FloatField()
    profit = models.FloatField()
    city = models.CharField(max_length=100)
    order_date = models.DateField()

    def __str__(self):
        return self.product_name