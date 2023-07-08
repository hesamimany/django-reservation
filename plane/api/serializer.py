from rest_framework import serializers
from plane.models import Plane, Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class PlaneSerializer(serializers.ModelSerializer):
    pTicket = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Plane
        fields = '__all__'
