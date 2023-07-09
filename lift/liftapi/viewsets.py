from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import F, Func

from liftapi.models import Elevator, ElevatorRequest, ElevatorSystem
from liftapi.serializers import ElevatorRequestSerializer,ElevatorSystemSerializer, ElevatorSerializer

class ElevatorRequestViewSet(viewsets.ModelViewSet):
    queryset = ElevatorRequest.objects.all()
    serializer_class = ElevatorRequestSerializer

    @action(detail=True, methods=['GET'])
    def requests_for_elevator(self, request, pk=None, elevator_system=None):
        try:
            elevator = Elevator.objects.filter(elevator_system=elevator_system).get(pk=pk)
            requests = self.queryset.filter(elevator=elevator)
            serializer = self.get_serializer(requests, many=True)
            return Response(serializer.data)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=404)






class ElevatorSystemViewSet(viewsets.ModelViewSet):
    """Viewset for ElevatorSystem"""

    queryset = ElevatorSystem.objects.all()
    serializer_class = ElevatorSystemSerializer

    @action(detail=False, methods=['GET'])
    def by_system_name(self, request, system_name=None):
        try:
            elevator_system = ElevatorSystem.objects.get(system_name=system_name)
            serializer = self.get_serializer(elevator_system)
            return Response(serializer.data)
        except ElevatorSystem.DoesNotExist:
            return Response({'error': 'Elevator system not found.'}, status=404)

    @action(detail=True, methods=['POST'])
    def request_elevator(self, request, pk=None):
        try:
            elevator_system = self.get_object()
            serializer = ElevatorRequestSerializer(data=request.data)

            requested_from_floor = serializer.initial_data['requested_from_floor']
            requested_to_floor = serializer.initial_data['requested_to_floor']

            # This query gets the closest elevator to the requested floor using Order By and ABS function
            closest_elevator = Elevator.objects.filter(elevator_system=elevator_system, is_operational=True).annotate(
                distance=Func(F('current_floor') - requested_from_floor, function='ABS')).order_by('distance').first()

            if closest_elevator:
                # Save properties to the closest elevator
                direction = (requested_to_floor - requested_from_floor) / abs(requested_to_floor - requested_from_floor)
                closest_elevator.direction = direction
                closest_elevator.current_floor = requested_to_floor
                closest_elevator.save()

                serializer.initial_data['elevator'] = closest_elevator.id

                if serializer.is_valid():
                    elevator_request = serializer.save()

                    return Response(ElevatorRequestSerializer(elevator_request).data)

        except ElevatorSystem.DoesNotExist:
            return Response({'error': 'Elevator system not found.'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=400)


"""Viewset class for Elevator model."""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets


class ElevatorViewSet(viewsets.ModelViewSet):
    """Viewset class for Elevator model."""

    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=['GET'])
    def status(self, request, pk=None, elevator_system=None):
        """Fetch the next destination floor for a given elevator."""
        try:
            elevator = self.queryset.filter(elevator_system=elevator_system).get(pk=pk)
            response = {}
            response['elevator_system'] = elevator_system
            response['data'] = self.get_serializer(elevator).data
            return Response(response)
        except Exception as e:
            return Response({'error': str(e)}, status=404)

    @action(detail=True, methods=['PATCH'])
    def update(self, request, pk=None, elevator_system=None):
        """Update elevator."""
        try:
            elevator = self.queryset.filter(elevator_system=elevator_system).get(pk=pk)
            serializer = self.get_serializer(elevator, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {}
                response['elevator_system'] = elevator_system
                response['data'] = serializer.data
                return Response(response)
        except Exception as e:
            return Response({'error': str(e)}, status=404)
