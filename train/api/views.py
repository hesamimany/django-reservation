from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from train.models import Train, Ticket
from .serializer import TicketSerializer, TrainSerializer


class TrainAPIView(APIView):
    throttle_classes = [AnonRateThrottle]
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk is not None:
            # Logic for retrieving a specific reservation by pk
            try:
                train = Train.objects.get(pk=pk)
                serializer = TrainSerializer(train)
                return Response(serializer.data)
            except Train.DoesNotExist:
                return Response(status=404)  # Return a not found response if the reservation doesn't exist
        else:
            # Logic for retrieving all reservations
            trains = Train.objects.all()
            serializer = TrainSerializer(trains, many=True)
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
        train_id = request.data.get('train_id')
        total = request.data.get('total')

        train = get_object_or_404(Train, pk=train_id)
        if not train.capacity != 0:
            return Response({'error': 'The train is full.'}, status=400)

        reservation = Ticket(
            user=request.user,
            train=train,
            total=total
        )
        reservation.save()
        if train.capacity - total < 0:
            return Response({'error': 'request is more that train capacity.'}, status=400)
        train.capacity -= total
        train.save()

        serializer = TicketSerializer(reservation)

        return Response(serializer.data)

    def __delete__(self, request, pk):
        try:
            reservation = Ticket.objects.get(pk=pk)

            train = reservation.train
            train.capacity += reservation.total
            train.save()

            reservation.delete()
            return Response(status=204)  # Return a success response if deletion is successful
        except Ticket.DoesNotExist:
            return Response(status=404)  # Return a not found response if the instance doesn't exist
