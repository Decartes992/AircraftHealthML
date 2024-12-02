from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/experiments/', views.get_experiment_list, name='experiment-list'),
    path('api/experiments/<str:experiment_id>/', views.get_experiment_data, name='experiment-data'),
]