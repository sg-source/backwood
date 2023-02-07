from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=15,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)])
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code
