from rest_framework import serializers
from hotel.models import Hotel, Room, HotelReservation


class HotelReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReservation
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    # reservations = HotelReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    reservation = HotelReservationSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'
