import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from monitoring.models import Flight, Stat

class Command(BaseCommand):
    help = 'Load flight_header and stats data'

    def handle(self, *args, **kwargs):
        # Load flight_header.csv
        with open(Path('monitoring/ml_models/data/NGAFID/raw/flight_header.csv'), 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                flight, created = Flight.objects.update_or_create(
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
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated Flight {flight.master_index}"))

        # Load stats.csv
        stats_to_create = []
        with open(Path('monitoring/ml_models/data/NGAFID/raw/stats.csv'), 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                flight = Flight.objects.filter(master_index=row['Master Index']).first()
                if not flight:
                    self.stderr.write(f"Flight {row['Master Index']} not found. Skipping stat.")
                    continue
                stat = Stat(
                    flight=flight,
                    key=row['Key'],
                    value=row['Value']
                )
                stats_to_create.append(stat)
        
        Stat.objects.bulk_create(stats_to_create)
        self.stdout.write(self.style.SUCCESS(f"Added {len(stats_to_create)} Stats to Flights"))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))