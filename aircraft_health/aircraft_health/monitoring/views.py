from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path

def dashboard_view(request):
    return render(request, 'monitoring/dashboard.html', {
        'debug': settings.DEBUG
    })

def get_experiment_list(request):
    """API endpoint to get list of experiments"""
    try:
        data_dir = Path("monitoring/ml_models/data/ADAPT/processed")
        files = [f.name for f in data_dir.glob("processed_*.csv")]
        experiments = [f.replace('processed_', '').replace('.csv', '') for f in files]
        return JsonResponse({'experiments': experiments})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_experiment_data(request, experiment_id):
    """API endpoint to get experiment data"""
    try:
        data_dir = Path("monitoring/ml_models/data/ADAPT/processed")
        
        # Read sensor data
        sensor_file = data_dir / f"processed_{experiment_id}.csv"
        with open(sensor_file) as f:
            sensor_data = f.read()
            
        # Read fault info
        fault_file = data_dir / f"fault_info_{experiment_id}.csv"
        with open(fault_file) as f:
            fault_info = f.read()
            
        return JsonResponse({
            'sensor_data': sensor_data,
            'fault_info': fault_info
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    def home_view(request):
        return render(request, 'home.html')