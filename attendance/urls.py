# urls.py
from django.urls import path
from .views import record_attendance, attendance_success, view_attendance

urlpatterns = [
    path('attendance/', record_attendance, name='record_attendance'),
    path('attendance/success/', attendance_success, name='attendance_success'),
    path('attendance/view/', view_attendance, name='view_attendance'),
]
