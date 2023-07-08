from rest_framework import serializers
from train.models import Train, Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TrainSerializer(serializers.ModelSerializer):
    tTicket = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Train
        fields = '__all__'
