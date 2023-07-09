from django.db import models

# Create your models here.

class ModelBase(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view')


class ElevatorRequest(ModelBase):
    """Model class for Elevator Requests"""

    elevator = models.ForeignKey('Elevator', on_delete=models.CASCADE)
    requested_from_floor = models.IntegerField()
    requested_to_floor = models.IntegerField()
    is_serviced = models.BooleanField(default=True)

    def __str__(self):
        return self.elevator + " requested from floor " + self.requested_from_floor

    class Meta:
        db_table = 'elevator_request'
        ordering = ['elevator']
        verbose_name_plural = 'elevator_requests'


class ElevatorSystem(ModelBase):
    """Model class for Elevator system"""

    system_name = models.CharField(max_length=100)
    number_of_elevators = models.IntegerField(default=1)
    number_of_floors = models.IntegerField(default=1)

    def __str__(self):
        return self.system_name

    class Meta:

        db_table = 'elevator_system'
        ordering = ['number_of_elevators']
        verbose_name_plural = 'elevator_systems'



class Elevator(ModelBase):
    """Model class for Elevator"""
    elevator_system = models.ForeignKey('ElevatorSystem', on_delete=models.CASCADE)
    elevator_number = models.IntegerField()
    current_floor = models.IntegerField(default=1)
    is_door_open = models.BooleanField(default=True)
    direction = models.CharField(choices=[(1, 'UP'), (-1, 'DOWN'), (0, 'STANDING STILL')], default=0, max_length=100)
    is_operational = models.BooleanField(default=True)

    def __str__(self):
        return self.elevator_number

    class Meta:

        db_table = 'elevator'
        ordering = ['elevator_number']
        verbose_name_plural = 'elevators'
