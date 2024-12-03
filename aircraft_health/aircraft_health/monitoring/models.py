from django.db import models

class Flight(models.Model):
    master_index = models.IntegerField(primary_key=True)
    before_after = models.CharField(max_length=10)  # 'before', 'after', 'same'
    date_diff = models.IntegerField()
    flight_length = models.IntegerField()
    label = models.CharField(max_length=255)
    hierarchy = models.CharField(max_length=255, blank=True, null=True)
    number_flights_before = models.IntegerField()

    def __str__(self):
        return f"Flight {self.master_index} - {self.label}"

class Stat(models.Model):
    flight = models.ForeignKey(Flight, related_name='stats', on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self):
        return f"Stat for Flight {self.flight.master_index} - {self.key}"
