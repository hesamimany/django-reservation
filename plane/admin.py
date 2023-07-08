from django.contrib import admin
from .models import Ticket, Plane

# Register your models here.


admin.site.register(Plane)
admin.site.register(Ticket)
