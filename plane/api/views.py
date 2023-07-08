from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

from plane.models import Plane, Ticket
from .serializer import TicketSerializer, PlaneSerializer


class PlaneAPIView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk is not None:
            # Logic for retrieving a specific reservation by pk
            try:
                plane = Plane.objects.get(pk=pk)
                serializer = PlaneSerializer(plane)
                return Response(serializer.data)
            except Plane.DoesNotExist:
                return Response(status=404)  # Return a not found response if the reservation doesn't exist
        else:
            # Logic for retrieving all reservations
            planes = Plane.objects.all()
            serializer = PlaneSerializer(planes, many=True)
            return Response(serializer.data)


class TicketAPIView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk is not None:
            # Logic for retrieving a specific reservation by pk
            try:
                ticket = Ticket.objects.get(pk=pk)
                serializer = TicketSerializer(ticket)
                return Response(serializer.data)
            except Ticket.DoesNotExist:
                return Response(status=404)  # Return a not found response if the reservation doesn't exist
        else:
            # Logic for retrieving all reservations
            reservations = Ticket.objects.all()
            serializer = TicketSerializer(reservations, many=True)
            return Response(serializer.data)

    def post(self, request):
        plane_id = request.data.get('plane_id')
        total = request.data.get('total')

        plane = get_object_or_404(Plane, pk=plane_id)
        if not plane.capacity != 0:
            return Response({'error': 'The plane is full.'}, status=400)

        reservation = Ticket(
            user=request.user,
            plane=plane,
            total=total
        )
        reservation.save()
        if plane.capacity - total < 0:
            return Response({'error': 'request is more that plane capacity.'}, status=400)
        plane.capacity -= total
        plane.save()

        serializer = TicketSerializer(reservation)

        return Response(serializer.data)

    def __delete__(self, request, pk):
        try:
            reservation = Ticket.objects.get(pk=pk)

            plane = reservation.plane
            plane.capacity += reservation.total
            plane.save()

            reservation.delete()
            return Response(status=204)  # Return a success response if deletion is successful
        except Ticket.DoesNotExist:
            return Response(status=404)  # Return a not found response if the instance doesn't exist
