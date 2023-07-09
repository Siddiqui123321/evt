from django.contrib import admin
from liftapi.models import Elevator, ElevatorRequest, ElevatorSystem
# Register your models here.

admin.site.register(Elevator)
admin.site.register(ElevatorRequest)
admin.site.register(ElevatorSystem)
