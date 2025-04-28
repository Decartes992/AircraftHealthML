from django.db import models

class Flight(models.Model):
    """
    Represents a flight record with various attributes.

    Attributes:
        master_index (int): A unique identifier for the flight.
        before_after (str): Indicates the state of the aircraft ('before', 'after', or 'same').
        date_diff (int): The difference in days from a reference date.
        flight_length (int): The duration of the flight in some unit (e.g., minutes, hours).
        label (str): A label associated with the flight, possibly indicating a condition.
        hierarchy (str, optional): Hierarchical information related to the flight.
        number_flights_before (int): The number of flights recorded before this one.
    """
    master_index = models.IntegerField(primary_key=True, db_index=True)
    before_after = models.CharField(max_length=10, db_index=True)  # 'before', 'after', 'same'
    date_diff = models.IntegerField(db_index=True)
    flight_length = models.IntegerField(db_index=True)
    label = models.CharField(max_length=255, db_index=True)
    hierarchy = models.CharField(max_length=255, blank=True, null=True)
    number_flights_before = models.IntegerField()

    def __str__(self):
        """Returns a string representation of the Flight instance."""
        return f"Flight {self.master_index} - {self.label}"

class Stat(models.Model):
    """
    Represents a statistical record associated with a flight.

    Attributes:
        flight (Flight): The flight instance this stat belongs to.
        key (str): The key identifying the type of statistic.
        value (float): The numerical value of the statistic.
    """
    flight = models.ForeignKey(Flight, related_name='stats', on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self):
        return f"Stat for Flight {self.flight.master_index} - {self.key}"
"""Returns a string representation of the Stat instance."""
