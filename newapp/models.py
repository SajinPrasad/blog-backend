from django.db import models

# Create your models here.


class TShirt(models.Model):
    brand = models.CharField(max_length=150)
    
    
class ColorVarient(models.Model):
    color = models.CharField(max_length=100)
    
class SizeVarient(models.Model):
    size = models.IntegerField()
    
class Price(models.Model):
    color = models.ForeignKey(ColorVarient, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVarient, on_delete=models.CASCADE)
    brand = models.ForeignKey(TShirt, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)