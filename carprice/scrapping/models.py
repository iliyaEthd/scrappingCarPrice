from django.db import models

# Create your models here.

#need model with
#year
#model
#package
#milage
#price

class Car(models.Model):
    vin = models.CharField(max_length=17, unique=True)
    model = models.CharField(max_length=30)
    package = models.CharField(max_length=30)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.IntegerField()
    
    