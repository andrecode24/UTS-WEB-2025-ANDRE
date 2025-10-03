from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.student_reports, name='student_reports'),
    path('create/', views.create_report, name='create_report'),
    path('<int:report_id>/edit/', views.edit_report, name='edit_report'),
    path('<int:report_id>/', views.view_report, name='view_report'),
]
