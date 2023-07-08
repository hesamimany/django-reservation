from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.

class Train(models.Model):
    start = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure = models.DateField()
    arrival = models.DateField()
    capacity = models.PositiveIntegerField(validators=[MaxValueValidator(200)])
    price = models.PositiveIntegerField(validators=[MaxValueValidator(999)])

    def __str__(self):
        return f"{self.start} to {self.destination}"


class Ticket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="tUser")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="tTicket")
    total = models.PositiveIntegerField(validators=[MaxValueValidator(20)])

    def __str__(self):
        return f"{self.user} got {self.total}"
