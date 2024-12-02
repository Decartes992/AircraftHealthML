from django.urls import path
from . import views

urlpatterns = [
    # Dashboard view for the React frontend
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # API endpoints for data
    path('api/experiments/', views.get_experiments, name='get_experiments'),
    path('api/experiments/<str:experiment_id>/', views.get_experiment_data, name='get_experiment_data'),
    path('api/experiments/', views.get_experiments, name='get_experiments'),
]
