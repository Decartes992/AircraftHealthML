# monitoring/views.py
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
import pandas as pd
import csv
import os

def dashboard_view(request):
    return render(request, 'monitoring/dashboard.html', {
        'debug': settings.DEBUG
    })

def get_experiment_list(request):
    """API endpoint to get list of experiments"""
    try:
        # Update path to point to raw data
        data_dir = Path("monitoring/ml_models/data/ADAPT/raw")
        # Get all .txt files
        files = [f.name for f in data_dir.glob("*.txt")]
        return JsonResponse({'experiments': files})
    except Exception as e:
        print(f"Error in get_experiment_list: {str(e)}")  # Debug print
        return JsonResponse({'error': str(e)}, status=500)
    
def get_experiment_data(request, experiment_id):
    """API endpoint to get experiment data"""
    try:
        data_dir = Path("monitoring/ml_models/data/ADAPT/raw")
        file_path = data_dir / experiment_id
        
        if not file_path.exists():
            return JsonResponse({'error': f'File not found: {experiment_id}'}, status=404)

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
        sensor_data = []
        for line in lines[2:]:
            values = line.strip().split('\t')
            if len(values) == len(headers) and values[0] == 'AntagonistData':
                row_data = {}
                for i, header in enumerate(headers):
                    row_data[header] = values[i]
                sensor_data.append(row_data)
            
        return JsonResponse({
            'sensor_data': sensor_data,
            'experiment_info': experiment_info
        })
    except Exception as e:
        print(f"Error processing experiment data: {str(e)}")  # Debug print
        return JsonResponse({'error': str(e)}, status=500)

def home_view(request):
    return render(request, 'monitoring/home.html')