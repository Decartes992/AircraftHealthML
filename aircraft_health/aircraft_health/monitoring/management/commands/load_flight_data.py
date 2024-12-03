import csv
from django.core.management.base import BaseCommand
from monitoring.models import Flight, Stat

class Command(BaseCommand):
    help = 'Load flight_header and stats data'

    def handle(self, *args, **kwargs):
        # Load flight_header.csv
        with open('monitoring/ml_models/data/NGAFID/raw/flight_header.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                flight, created = Flight.objects.get_or_create(
                    master_index=row['Master Index'],
                    defaults={
                        'before_after': row['before_after'],
                        'date_diff': row['date_diff'],
                        'flight_length': row['flight_length'],
                        'label': row['label'],
                        'hierarchy': row.get('hierarchy', ''),
                        'number_flights_before': row['number_flights_before']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Flight {flight.master_index}"))

        # Load stats.csv
        with open('monitoring/ml_models/data/NGAFID/raw/stats.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                flight = Flight.objects.get(master_index=row['Master Index'])
                Stat.objects.create(
                    flight=flight,
                    key=row['Key'],
                    value=row['Value']
                )
                self.stdout.write(self.style.SUCCESS(f"Added Stat to Flight {flight.master_index}"))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))