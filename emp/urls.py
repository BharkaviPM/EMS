from django.contrib import admin
from django.urls import path,include
from .views import emp_home, add_emp, delete_emp, update_emp, do_update_emp, login_view, register_view, admin_dashboard, manager_dashboard, user_dashboard, mark_attendance, calculate_performance, attendance_dashboard,performance_dashboard, faq_list, update_attendance

urlpatterns = [
    path("home/", emp_home, name='emp_home'),
    path("add-emp/", add_emp, name='add_emp'),
    path("delete-emp/<int:emp_id>/", delete_emp, name='delete_emp'),
    path("update-emp/<int:emp_id>/", update_emp, name='update_emp'),
    path("do-update-emp/<int:emp_id>/", do_update_emp, name='do_update_emp'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('manager/dashboard/', manager_dashboard, name='manager_dashboard'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('performance_dashboard/', performance_dashboard, name='performance_dashboard'),
    path('attendance/dashboard/', attendance_dashboard, name='attendance_dashboard'),
    path('calculate_performance/', calculate_performance, name='calculate_performance'),
    path('faq_list/', faq_list, name='faq_list'),
    path('update-attendance/', update_attendance, name='update_attendance'),
]
