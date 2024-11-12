from django.shortcuts import render, redirect
from .models import Employee, Attendance
from .forms import AttendanceForm

def record_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_success')  # Redirect after successful post
    else:
        form = AttendanceForm()

    employees = Employee.objects.all()  # Get all employees for the dropdown
    return render(request, 'record_attendance.html', {'form': form, 'employees': employees})

def attendance_success(request):
    return render(request, 'attendance_success.html')

def view_attendance(request):
    attendance_records = Attendance.objects.all().order_by('-date')
    return render(request, 'view_attendance.html', {'attendance_records': attendance_records})

