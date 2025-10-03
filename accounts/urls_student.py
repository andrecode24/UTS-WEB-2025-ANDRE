from django.urls import path
from . import views_student

app_name = 'student'

urlpatterns = [
    path('register/', views_student.register, name='register'),
    path('profile/', views_student.profile, name='profile'),
    path('profile/edit/', views_student.edit_profile, name='edit_profile'),
    path('dashboard/', views_student.dashboard, name='dashboard'),
    path('jobs/', views_student.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views_student.job_detail, name='job_detail'),
    path('applications/', views_student.my_applications, name='applications'),
    path('reports/', views_student.reports, name='reports'),
    path('internship/confirm/', views_student.confirm_internship, name='confirm_internship'),
]
