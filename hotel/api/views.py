from django.db.models import F, Sum, Q
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

from hotel.models import Hotel, Room, HotelReservation
from .serializer import HotelReservationSerializer, HotelSerializer


class HotelFilterView(APIView):
    def post(self, request):
        city = request.data.get('city')
        entry_date = request.data.get('entry')
        exit_date = request.data.get('exit')
        total = request.data.get('total')
        my_data = {}
        reserved = HotelReservation.objects.all().filter(
            Q(check_in__lte=entry_date, check_out__gte=entry_date) | Q(check_in__lte=exit_date,
                                                                       check_out__gte=exit_date)).values()
        capacity = HotelReservation.objects.values('hotel').annotate(capacity=Sum(F('room__num_beds'))).filter(
            hotel__city=city)

        index = 0
        # print(reserved)
        list = []
        price = []
        for hotel in Hotel.objects.all():
            if hotel.city == city:
                res = HotelReservation.objects.all().values().filter(hotel_id=hotel.pk).first()
                price.append(Room.objects.all().values().get(pk=res.get("room_id")).get("price"))
                for reserve in reserved:
                    if hotel.pk == reserve.get("hotel_id"):
                        hotel.capacity -= Room.objects.all().values().get(pk=reserve.get("room_id")).get("num_beds")

                list.append(hotel)

        print(list)

        serializer = HotelSerializer(list, many=True, partial=True)
        # if serializer.is_valid():
        #     print(serializer.validated_data)
        # else:
        #     print("hehe")

        # print(capacity)

        # for hotel in capacity:
        #     print(hotel)
        #     serializer = HotelSerializer(Hotel.objects.all().get(pk=hotel['hotel']))
        #     Hotel.objects.all().get(pk=hotel['hotel'])
        #     room = HotelReservation.objects.all().filter(hotel=Hotel.objects.all().get(pk=hotel['hotel'])).exclude(
        #         room__bed_type="default")
        #     print(room.get("price"))
        #     print(hotel['capacity'])
        #     my_data[index] = [serializer.data, int(hotel['capacity'])]
        #     index += 1

        # capacity =
        dic = serializer.data

        index = 0
        for _ in dic:
            dic[index]["price"] = price[index]
            index += 1
            # print(dic[index])

        return Response(dic, status=200)


class HotelAPIView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        # print(pk, end="\n\n\n")
        if pk is not None:
            # Logic for retrieving a specific reservation by pk
            try:
                hotel = Hotel.objects.get(pk=pk)
                serializer = HotelSerializer(hotel)
                return Response(serializer.data)
            except Hotel.DoesNotExist:
                return Response(status=404)  # Return a not found response if the reservation doesn't exist
        else:
            # Logic for retrieving all reservations
            hotels = Hotel.objects.all()
            serializer = HotelSerializer(hotels, many=True)
            return Response(serializer.data)


class HotelReservationAPIView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        # print(pk, end="\n\n\n")
        if pk is not None:
            # Logic for retrieving a specific reservation by pk
            try:
                reservation = HotelReservation.objects.get(pk=pk)
                serializer = HotelReservationSerializer(reservation)
                return Response(serializer.data)
            except HotelReservation.DoesNotExist:
                return Response(status=404)  # Return a not found response if the reservation doesn't exist
        else:
            # Logic for retrieving all reservations
            reservations = HotelReservation.objects.all()
            serializer = HotelSerializer(reservations, many=True)
            return Response(serializer.data)

    def post(self, request):
        room_id = request.data.get('room_id')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')

        room = get_object_or_404(Room, pk=room_id)
        if not room.is_available:
            return Response({'error': 'The room is not available.'}, status=400)

        hotel = room.reservations_room.hotel
        # hotel = Hotel.objects.all().first()

        reservation = HotelReservation(
            user=request.my_user,
            room=room,
            hotel=hotel,
            check_in=check_in,
            check_out=check_out
        )
        reservation.save()

        numBeds = room.num_beds
        # room.hotel.capacity -= numBeds
        # room.hotel.save()

        room.is_available = False
        room.save()

        serializer = HotelReservationSerializer(reservation)

        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            reservation = HotelReservation.objects.get(pk=pk)

            room = reservation.room
            hotel = reservation.hotel
            hotel.capacity += room.num_beds
            hotel.save()
            room.is_available = True
            room.save()

            reservation.delete()
            return Response(status=204)  # Return a success response if deletion is successful
        except HotelReservation.DoesNotExist:
            return Response(status=404)  # Return a not found response if the instance doesn't exist
