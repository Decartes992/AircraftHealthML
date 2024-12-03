from django.urls import path, re_path
from .views import FlightListView, FlightDetailView
from . import views

urlpatterns = [
    path('api/experiments/', views.get_experiment_list, name='experiment-list'),
    path('api/experiments/<str:experiment_id>/', views.get_experiment_data, name='experiment-data'),
    path('api/ngafid/flight_data/', FlightListView.as_view(), name='flight-list'),
    path('api/ngafid/flight_data/<int:flight_id>/', FlightDetailView.as_view(), name='flight-detail'),
    re_path(r'^.*$', views.dashboard_view, name='dashboard'),
]