from django.shortcuts import render
from django.http import JsonResponse
from .ml_models.utils.data_loader import ADAPTDataLoader
from pathlib import Path

def get_experiments(request):
    loader = ADAPTDataLoader('/path/to/your/processed/data')  # Replace with actual path
    experiments = loader.get_experiment_list()
    return JsonResponse({'experiments': experiments})

def get_experiment_data(request, experiment_id):
    loader = ADAPTDataLoader('/path/to/your/processed/data')  # Replace with actual path
    data = loader.load_experiment(experiment_id)
    return JsonResponse(data)

def get_experiments(request):
    data_dir = Path("path/to/data/ADAPT/raw")  # Adjust path as needed
    experiments = [f.name for f in data_dir.glob("*.txt")]
    return JsonResponse({"experiments": experiments})