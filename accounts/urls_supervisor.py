from django.urls import path
from . import views_supervisor

app_name = 'supervisor'

urlpatterns = [
    path('dashboard/', views_supervisor.dashboard, name='dashboard'),
    path('students/', views_supervisor.students, name='students'),
    path('evaluations/', views_supervisor.evaluations, name='evaluations'),
    path('evaluations/<int:evaluation_id>/', views_supervisor.evaluation_form, name='evaluation_form'),
    path('evaluations/<int:evaluation_id>/preview/', views_supervisor.evaluation_preview, name='evaluation_preview'),
]
