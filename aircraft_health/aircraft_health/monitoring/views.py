# monitoring/views.py
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
import pandas as pd
import csv
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Flight
from .serializers import FlightSerializer
import logging
from django.db.models import F, Avg, Max, Min, Count
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI environments
import matplotlib.pyplot as plt
import io
import base64
from rest_framework.decorators import api_view
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np

logger = logging.getLogger(__name__)

def dashboard_view(request):
    """Renders the main dashboard HTML page."""
    return render(request, 'monitoring/dashboard.html', {
        'debug': settings.DEBUG
    })

def get_experiment_list(request):
    """
    API endpoint to get a list of available experiment files from the ADAPT raw data directory.

    Returns:
        JsonResponse: A JSON response containing a list of experiment filenames.
                      Returns an error message with status 500 if an exception occurs.
    """
    try:
        # Update path to point to raw data
        data_dir = Path("monitoring/ml_models/data/ADAPT/raw")
        # Get all .txt files
        files = [f.name for f in data_dir.glob("*.txt")]
        return JsonResponse({'experiments': files})
    except Exception as e:
        logger.error(f"Error in get_experiment_list: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def get_experiment_data(request, experiment_id):
    """
    API endpoint to get detailed data for a specific experiment.

    Args:
        request: The HTTP request object.
        experiment_id (str): The filename of the experiment data to retrieve.

    Returns:
        JsonResponse: A JSON response containing the sensor data and experiment information.
                      Returns an error message with status 404 if the file is not found,
                      status 400 if the file format is invalid, or status 500 if an
                      unexpected error occurs.
    """
    try:
        data_dir = Path("monitoring/ml_models/data/ADAPT/raw")
        file_path = data_dir / experiment_id
        
        if not file_path.exists():
            return JsonResponse({'error': f'File not found: {experiment_id}'}, status=404)

        # Validate file format
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if len(lines) < 2:
                    raise ValueError("File format invalid: Insufficient lines.")
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)

        # Read the raw file content
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Process experiment info (first line)
        experiment_info = {}
        info_parts = lines[0].strip().split('\t')
        if len(info_parts) > 2:  # Ensure there's enough data
            experiment_info = {
                'type': info_parts[0],
                'operationCode': info_parts[4].split('=')[1].strip() if len(info_parts) > 4 else '',
                'faultType': info_parts[8].split('=')[1].strip() if len(info_parts) > 8 else '',
                'faultMode': info_parts[9].split('=')[1].strip() if len(info_parts) > 9 else '',
                'faultLocation': info_parts[10].split('=')[1].strip() if len(info_parts) > 10 else ''
            }
        
        # Get headers (second line)
        headers = lines[1].strip().split('\t')
        
        # Process sensor data (remaining lines)
        df = pd.DataFrame([line.strip().split('\t') for line in lines[2:]], columns=headers)
        df = df[df['SensorData'] == 'AntagonistData']
        sensor_data = df.to_dict(orient='records')
            
        return JsonResponse({
            'sensor_data': sensor_data,
            'experiment_info': experiment_info
        })
    except Exception as e:
        logger.error(f"Error processing experiment data: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_unique_labels(request):
    """
    API endpoint to get a list of unique labels from the Flight model.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing a list of unique labels.
    """
    logger.debug("Fetching unique labels")
    labels = Flight.objects.values_list('label', flat=True).distinct()
    logger.debug(f"Unique labels fetched: {labels}")
    return JsonResponse(list(labels), safe=False)

@api_view(['GET'])
def filter_flights_by_label(request, label):
    """
    API endpoint to filter flights by a specific label.

    Args:
        request: The HTTP request object.
        label (str): The label to filter flights by.

    Returns:
        JsonResponse: A JSON response containing a list of filtered flights.
    """
    flights = Flight.objects.filter(label=label).values(
        'master_index', 'before_after', 'date_diff', 'flight_length',
        'number_flights_before', 'hierarchy', 'stats'
    )
    return JsonResponse(list(flights), safe=False)

@api_view(['GET'])
def flights_by_label(request, label):
    """
    API endpoint to retrieve flight data and generate visualizations for a specific label.

    Args:
        request: The HTTP request object.
        label (str): The label to filter flights by.

    Returns:
        JsonResponse: A JSON response containing flight entries and base64 encoded visualizations.
                      Returns an error message with status 500 if an exception occurs.
    """
    try:
        logger.debug(f"Fetching flights for label: {label}")
        flights = Flight.objects.filter(label=label).values(
            "master_index", "before_after", "date_diff", "flight_length", "number_flights_before"
        )
        df = pd.DataFrame(list(flights))
        logger.debug(f"DataFrame created with {len(df)} entries")

        visualizations = {}

        # Time-series plot for flight lengths
        plt.figure(figsize=(10, 6))
        plt.plot(df["master_index"], df["flight_length"], marker="o", linestyle="-")
        plt.title(f"Flight Lengths for Label: {label}")
        plt.xlabel("Master Index")
        plt.ylabel("Flight Length")
        plt.grid()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        visualizations["flight_length_plot"] = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        plt.close()
        logger.debug("Time-series plot created")

        # Histogram for flight lengths
        plt.figure(figsize=(10, 6))
        plt.hist(df["flight_length"], bins=20, alpha=0.7, color="blue")
        plt.title(f"Flight Length Distribution for Label: {label}")
        plt.xlabel("Flight Length")
        plt.ylabel("Frequency")
        plt.grid()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        visualizations["flight_length_histogram"] = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        plt.close()
        logger.debug("Histogram created")

        response = {
            "label": label,
            "entries": df.to_dict(orient="records"),
            "visualizations": visualizations,
        }
        logger.debug("Response prepared")

        return JsonResponse(response)
    except Exception as e:
        logger.error(f"Error fetching flights for label {label}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def flight_data_by_label(request, label):
    """
    API endpoint to get serialized flight data filtered by label.

    Args:
        request: The HTTP request object.
        label (str): The label to filter flights by.

    Returns:
        Response: A DRF Response containing serialized flight data.
    """
    flights = Flight.objects.filter(label=label).order_by('master_index')
    serialized_flights = FlightSerializer(flights, many=True)
    return Response(serialized_flights.data)

@api_view(['GET'])
def flight_insights(request, label):
    """
    API endpoint to get basic statistical insights for flights filtered by label.

    Args:
        request: The HTTP request object.
        label (str): The label to filter flights by.

    Returns:
        JsonResponse: A JSON response containing average, max, and min flight lengths.
                      Returns an error message with status 500 if an exception occurs.
    """
    logger.debug(f"Fetching insights for label: {label}")
    try:
        flights = Flight.objects.filter(label=label)
        logger.debug(f"Number of flights found: {flights.count()}")
        
        avg_length = flights.aggregate(Avg('flight_length'))['flight_length__avg']
        max_length = flights.aggregate(Max('flight_length'))['flight_length__max']
        min_length = flights.aggregate(Min('flight_length'))['flight_length__min']
        
        logger.debug(f"Average flight length: {avg_length}")
        logger.debug(f"Max flight length: {max_length}")
        logger.debug(f"Min flight length: {min_length}")
        
        return JsonResponse({
            "average": avg_length,
            "max": max_length,
            "min": min_length,
        })
    except Exception as e:
        logger.error(f"Error fetching insights for label {label}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def grouped_flight_data(request):
    """
    API endpoint to get grouped flight data for visualization.

    Args:
        request: The HTTP request object containing the 'label' query parameter.

    Returns:
        Response: A DRF Response containing scatter and histogram data.
    """
    label = request.query_params.get('label')
    flights = Flight.objects.filter(label=label)

    # Process relevant visualization data
    scatter_data = [{"x": f.master_index, "y": f.flight_length} for f in flights]
    histogram_data = [f.flight_length for f in flights]

    return Response({
        "scatter_data": scatter_data,
        "histogram_data": histogram_data,
    })

@api_view(['GET'])
def unique_labels(request):
    """
    API endpoint to get unique labels and their counts from the Flight model.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A DRF Response containing a list of unique labels and their counts.
    """
    labels = Flight.objects.values('label').annotate(count=Count('label'))
    return Response(labels)

@api_view(['GET'])
def preprocessed_flight_data(request, label):
    """
    API endpoint to get preprocessed flight data and insights for a specific label.

    Args:
        request: The HTTP request object.
        label (str): The label to filter flights by.

    Returns:
        Response: A DRF Response containing scatter data, histogram data, and insights.
    """
    flights = Flight.objects.filter(label=label)
    scatter_data = [{"x": f.master_index, "y": f.flight_length} for f in flights]
    histogram_data = [f.flight_length for f in flights]

    insights = {
        "average": sum(histogram_data) / len(histogram_data),
        "max": max(histogram_data),
        "min": min(histogram_data),
    }

    return Response({
        "scatter_data": scatter_data,
        "histogram_data": histogram_data,
        "insights": insights,
    })

@require_http_methods(["GET"])
def get_anomaly_results(request):
    """
    API endpoint to get anomaly detection results from ADAPT and NGAFID models.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing anomaly detection results for ADAPT and NGAFID.
                      Returns an error message with status 404 if result files are not found,
                      or status 500 if an unexpected error occurs.
    """
    try:
        # Update path to match your project structure
        results_dir = Path('monitoring/ml_models/Models/results')  # Adjust this path
        
        # Add error handling for file existence
        adapt_results_path = results_dir / 'adapt_results.json'
        ngafid_results_path = results_dir / 'ngafid_results.json'
        
        if not adapt_results_path.exists() or not ngafid_results_path.exists():
            return JsonResponse(
                {'error': 'Result files not found'}, 
                status=404
            )

        # Read ADAPT results
        with open(adapt_results_path, 'r') as f:
            adapt_data = json.load(f)
            
        # Read NGAFID results    
        with open(ngafid_results_path, 'r') as f:
            ngafid_data = json.load(f)
            
        # Handle NaN values
        adapt_data = handle_nan_values(adapt_data)
        ngafid_data = handle_nan_values(ngafid_data)
        
        # Format response data
        response_data = {
            'adapt': {
                'timeSeriesData': adapt_data['timeSeriesData'],
                'anomalies': adapt_data['anomalies'],
                'anomalyScores': adapt_data['anomalyScores'],
                'summary': adapt_data['summary']
            },
            'ngafid': {
                'maintenancePredictions': [
                    {
                        'flightId': flight_id,
                        'maintenanceProbability': score,
                        'needsMaintenance': anomaly == -1,
                        'anomalyScore': score
                    }
                    for flight_id, score, anomaly in zip(
                        ngafid_data['flightData'],
                        ngafid_data['anomalyScores'],
                        ngafid_data['anomalies']
                    )
                ],
                'summary': ngafid_data['summary']
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error fetching anomaly results: {str(e)}")
        return JsonResponse(
            {'error': 'Failed to fetch anomaly detection results'}, 
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def update_threshold(request):
    """
    API endpoint to update the anomaly detection threshold.

    Args:
        request: The HTTP request object containing the new threshold in the request body.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the update.
                      Returns an error message with status 400 if the threshold is not provided,
                      or status 500 if an unexpected error occurs.
    """
    try:
        data = json.loads(request.body)
        threshold = data.get('threshold')
        
        if threshold is None:
            return JsonResponse(
                {'error': 'Threshold value is required'}, 
                status=400
            )
            
        # Here you would typically update your model's threshold
        # and potentially rerun detection
        
        return JsonResponse({
            'message': 'Threshold updated successfully',
            'threshold': threshold
        })
        
    except Exception as e:
        logger.error(f"Error updating threshold: {str(e)}")
        return JsonResponse(
            {'error': 'Failed to update threshold'}, 
            status=500
        )

@require_http_methods(["GET"])
def get_historical_data(request):
    """
    API endpoint to get historical anomaly data within a specified date range.

    Args:
        request: The HTTP request object containing 'start' and 'end' query parameters.

    Returns:
        JsonResponse: A JSON response containing historical anomaly data for ADAPT and NGAFID.
                      Returns an error message with status 400 if start or end dates are not provided,
                      or status 500 if an unexpected error occurs.
    """
    try:
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        
        if not start_date or not end_date:
            return JsonResponse(
                {'error': 'Start and end dates are required'}, 
                status=400
            )
            
        # Here you would typically query your historical data
        # based on the date range
        
        return JsonResponse({
            'adapt': [],  # Add historical ADAPT data
            'ngafid': []  # Add historical NGAFID data
        })
        
    except Exception as e:
        logger.error(f"Error fetching historical data: {str(e)}")
        return JsonResponse(
            {'error': 'Failed to fetch historical data'}, 
            status=500
        )

class FlightListView(generics.ListAPIView):
    """
    API view to list Flight instances with filtering and ordering capabilities.
    """
    queryset = Flight.objects.prefetch_related('stats').all().order_by('master_index')  # Add ordering
    serializer_class = FlightSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['before_after', 'label']
    search_fields = ['label']
    ordering_fields = ['date_diff', 'flight_length']

class FlightDetailView(APIView):
    """
    API view to retrieve details for a specific Flight instance.
    """
    def get(self, request, flight_id):
        """
        Retrieves a single Flight instance by its master_index.

        Args:
            request: The HTTP request object.
            flight_id (int): The master_index of the Flight to retrieve.

        Returns:
            Response: A DRF Response containing the serialized Flight data.
                      Returns a 404 response if the Flight is not found,
                      or a 500 response if an unexpected error occurs.
        """
        try:
            flight = Flight.objects.prefetch_related('stats').get(master_index=flight_id)
            serializer = FlightSerializer(flight)
            return Response({'experiment_info': serializer.data})
        except Flight.DoesNotExist:
            logger.error(f"Flight not found: {flight_id}")
            return Response({'error': f'Flight {flight_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def home_view(request):
    """Renders the home HTML page."""
    return render(request, 'monitoring/home.html')

def handle_nan_values(data):
    """
    Recursively replace NaN values with None in a dictionary or list.

    Args:
        data: The data structure (dict or list) to process.

    Returns:
        The data structure with NaN values replaced by None.
    """
    if isinstance(data, dict):
        return {k: handle_nan_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [handle_nan_values(v) for v in data]
    elif isinstance(data, float) and np.isnan(data):
        return None
    else:
        return data