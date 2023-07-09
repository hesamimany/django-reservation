from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from account.manager import UserManager
from account.models import CustomUser


# Create your models here.


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_type = models.CharField(max_length=50)
    bed_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_beds = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.room_type} / {self.num_beds} Beds'


class HotelReservation(models.Model):
    my_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField()

    def __str__(self):
        return f'{self.my_user} got {self.room}'
