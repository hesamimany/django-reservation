from django.contrib import admin
from .models import Ticket, Train

# Register your models here.


admin.site.register(Train)
admin.site.register(Ticket)