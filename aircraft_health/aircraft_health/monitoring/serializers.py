from rest_framework import serializers
from .models import Flight, Stat

class StatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Stat model.

    Serializes the 'key' and 'value' fields of a Stat instance.
    """
    class Meta:
        model = Stat
        fields = ['key', 'value']

class FlightSerializer(serializers.ModelSerializer):
    """
    Serializer for the Flight model.

    Includes nested serialization for related Stat instances.
    """
    stats = StatSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ['master_index', 'before_after', 'date_diff', 'flight_length', 'label', 'hierarchy', 'number_flights_before', 'stats']