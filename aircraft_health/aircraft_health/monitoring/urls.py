from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/experiments/', views.get_experiment_list, name='experiment-list'),
    path('api/experiments/<str:experiment_id>/', views.get_experiment_data, name='experiment-data'),
    re_path(r'^.*$', views.dashboard_view, name='dashboard'),
]