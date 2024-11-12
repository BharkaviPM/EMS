from django.shortcuts import redirect, render
from django.http import HttpResponse

from attendance import models
from .models import Emp
from .models import Attendance, Performance, FAQ
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.db.models import Sum, F
from datetime import timedelta
from django.db.models import Avg
import plotly.express as px # type: ignore
from plotly.offline import plot # type: ignore
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.utils import timezone
from django.http import JsonResponse


@login_required
def admin_dashboard(request):
    emps = Emp.objects.all()
    sort_by = request.GET.get('sort_by', 'name')  # Default sorting by 'name'
    order = request.GET.get('order', 'asc')  # Default sorting order 'asc' (ascending)

    # Filter by department if provided
    department = request.GET.get('department')  # Get department from the request
    if department:
        emps = emps.filter(department=department)  # Filter employees by department

    # Filter by project if provided
    project = request.GET.get('project')  # Get project from the request
    if project:
        emps = emps.filter(emp_project=project)  # Filter employees by project

    if order == 'desc':
        sort_by = f'-{sort_by}'  # Adding '-' before the field will sort in descending order.

    emps = emps.order_by(sort_by)

    return render(request, "emp/admin_dashboard.html", {
        'emps': emps,
        'current_sort_by': sort_by,
        'current_order': order,
        'current_department': department,
        'current_project': project,  # Pass the current project filter to the template
        'current_user': request.user,  # Pass the logged-in user to the template
    })

@login_required
def manager_dashboard(request):
    user = request.user
    userprofile = Emp.objects.get(user=user)
    emps = Emp.objects.all()  # Fetch all employees for the manager view
    
    return render(request, 'emp/manager_dashboard.html', {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'emps': emps,
    })

@login_required
def user_dashboard(request):
    user = request.user
    userprofile = Emp.objects.get(user=user)

    # Filter employees to only include the logged-in user's details
    emps = Emp.objects.filter(name=user.username)

    # Debugging statements
    print(f'User: {user.username}, Employee Count: {emps.count()}')

    return render(request, 'emp/user_dashboard.html', {
        'user': user,
        'userprofile': userprofile,
        'emps': emps,
    })

@login_required
def emp_home(request):
    emps = Emp.objects.all()
    sort_by = request.GET.get('sort_by', 'name')  # Default sorting by 'name'
    order = request.GET.get('order', 'asc')  # Default sorting order 'asc' (ascending)

    # Filter by department if provided
    department = request.GET.get('department')  # Get department from the request
    if department:
        emps = emps.filter(department=department)  # Filter employees by department

    # Filter by project if provided
    project = request.GET.get('project')  # Get project from the request
    if project:
        emps = emps.filter(emp_project=project)  # Filter employees by project

    if order == 'desc':
        sort_by = f'-{sort_by}'  # Adding '-' before the field will sort in descending order.

    emps = emps.order_by(sort_by)

    return render(request, "emp/home.html", {
        'emps': emps,
        'current_sort_by': sort_by,
        'current_order': order,
        'current_department': department,
        'current_project': project,  # Pass the current project filter to the template
        'current_user': request.user,  # Pass the logged-in user to the template
    })


def new_func(request, emps):
    return render(request,"emp/home.html",{'emps':emps})


def add_emp(request):
    if request.method=="POST":
        emp_name=request.POST.get("emp_name")
        emp_id=request.POST.get("emp_id")
        emp_phone=request.POST.get("emp_phone")
        emp_address=request.POST.get("emp_address")
        emp_working=request.POST.get("emp_working")
        emp_department=request.POST.get("emp_department")
        emp_age = request.POST.get("emp_age")
        emp_project = request.POST.get("emp_project")
        e = Emp(
            name=emp_name,
            emp_id=emp_id,
            phone=emp_phone,
            address=emp_address,
            working=emp_working,
            department=emp_department,
            age=emp_age,
            project=emp_project
        )
        if emp_working is None:
            e.working=False
        else:
            e.working=True
        e.save()
        return redirect("/emp/home/")
    return render(request,"emp/add_emp.html",{})

def delete_emp(request,emp_id):
    emp=Emp.objects.get(pk=emp_id)
    emp.delete()
    return redirect("/emp/home/")

def update_emp(request,emp_id):
    emp=Emp.objects.get(pk=emp_id)
    print("Yes Bhai")
    return render(request,"emp/update_emp.html",{
        'emp':emp
    })

def do_update_emp(request,emp_id):
    if request.method=="POST":
        emp_name=request.POST.get("emp_name")
        emp_id_temp=request.POST.get("emp_id")
        emp_phone=request.POST.get("emp_phone")
        emp_address=request.POST.get("emp_address")
        emp_working=request.POST.get("emp_working")
        emp_department=request.POST.get("emp_department")
        emp_age = request.POST.get("emp_age")
        emp_project = request.POST.get("emp_project")

        e=Emp.objects.get(pk=emp_id)

        e.name=emp_name
        e.emp_id=emp_id_temp
        e.phone=emp_phone
        e.address=emp_address
        e.department=emp_department
        e.age=emp_age
        e.project=emp_project

        e.save()
        if emp_working is None:
            e.working=False
        else:
            e.working=True
        e.save()
    return redirect("/emp/home/")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Fetch the user's role from the UserProfile model
            user_profile = Emp.objects.get(user=user)  # Assuming a OneToOneField relationship
            
            # Redirect based on user role
            if user_profile.role == 'admin':
                return redirect('admin_dashboard')  # Change to your admin dashboard URL
            elif user_profile.role == 'manager':
                return redirect('manager_dashboard')  # Change to your manager dashboard URL
            else:
                return redirect('user_dashboard')  # Change to your user dashboard URL
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'emp/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']  # Get the selected role from the form

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                Emp.objects.create(user=user, role=role)  # Create user profile with role
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'emp/register.html')

def mark_attendance(request):
    if request.method == 'POST':
        # Process attendance form data for each employee
        for emp in Emp.objects.all():
            check_in_time = request.POST.get(f'check_in_{emp.id}')
            check_out_time = request.POST.get(f'check_out_{emp.id}')
            attendance_status = request.POST.get(f'attendance_status_{emp.id}')

            # Get or create attendance entry for the employee on today's date
            attendance, created = Attendance.objects.get_or_create(employee=emp, date=date.today())

            # Update attendance fields if provided
            if check_in_time:
                attendance.check_in = check_in_time
            if check_out_time:
                attendance.check_out = check_out_time
            if attendance_status:
                attendance.status = attendance_status

            # Save changes to attendance record
            attendance.save()

        messages.success(request, "Attendance marked successfully.")
        return redirect('attendance_dashboard')  # Redirect to dashboard after marking attendance

    # If GET request, pass all employees to the template
    emps = Emp.objects.all()
    return render(request, 'emp/mark_attendance.html', {'emps': emps})

def attendance_dashboard(request):
    # Get current date or provided date
    current_date = request.GET.get('date', date.today())
    department_filter = request.GET.get('department', '')

    # Filter attendance based on date and department (if provided)
    if department_filter:
        attendances = Attendance.objects.filter(date=current_date, department=department_filter)
    else:
        attendances = Attendance.objects.filter(date=current_date)

    # Pass attendance data and the current date to the template
    return render(request, 'emp/attendance_dashboard.html', {
        'attendances': attendances,
        'current_date': current_date,
        'current_department': department_filter
    })
def performance_dashboard(request):
    employees = Emp.objects.all()

    performance_data = []
    employee_names = []
    total_scores = []

    # Collect performance data
    for employee in employees:
        performance, _ = Performance.objects.get_or_create(employee=employee)
        performance.calculate_overall_score()  # Update score

        employee_names.append(employee.name)
        total_scores.append(performance.total_score)

        performance_data.append({
            'employee': employee,
            'performance': performance,
        })

    # Sort and get top 10
    performance_data_sorted = sorted(performance_data, key=lambda x: x['performance'].total_score, reverse=True)[:10]

    # Generate graph
    plt.figure(figsize=(12, 6))
    bars = plt.bar(employee_names, total_scores, color='skyblue', edgecolor='black')
    plt.xlabel('Employee', fontsize=14)
    plt.ylabel('Performance Score', fontsize=14)
    plt.title('Employee Performance Scores', fontsize=16)
    plt.ylim(0, 100)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right', fontsize=12)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height:.1f}', ha='center', fontsize=10, color='black')

    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()

    context = {
        'performance_data': performance_data,
        'performance_data_sorted': performance_data_sorted,
        'plot_data': plot_data,
    }
    return render(request, 'emp/performance_dashboard.html', context)
def calculate_performance(employee):
    # Fetch or create a Performance instance for the employee
    performance, _ = Performance.objects.get_or_create(employee=employee)

    # Define weights for each metric
    attendance_weight = 1
    project_weight = 5
    publication_weight = 3
    meeting_weight = 1  # Example, you can adjust based on your logic
    overtime_weight = 0.5  # Example, you can adjust based on your logic

    # Calculate attendance score (count how many days the employee was present)
    attendance_score = Attendance.objects.filter(employee=employee, status='Present').count()

    # Get project, publication, meeting, and overtime scores (adjust as per your logic)
    project_score = performance.project_score or 0
    publication_score = performance.publication_score or 0
    meeting_score = performance.meeting_score or 0
    overtime_score = performance.overtime_score or 0

    # Calculate the overall score
    total_score = (
        (attendance_score * attendance_weight) +
        (project_score * project_weight) +
        (publication_score * publication_weight) +
        (meeting_score * meeting_weight) +
        (overtime_score * overtime_weight)
    )

    # Save the individual scores and the total score to the Performance instance
    performance.attendance_score = attendance_score
    performance.project_score = project_score
    performance.publication_score = publication_score
    performance.meeting_score = meeting_score
    performance.overtime_score = overtime_score
    performance.total_score = total_score
    performance.save()

    return performance

def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'emp/faq_list.html',{'faqs':faqs})
def update_attendance(request):
    department = request.GET.get('department', '')
    date = request.GET.get('date', '')

    attendances = Attendance.objects.all()

    # Filter by department and date if provided
    if department:
        attendances = attendances.filter(employee__department=department)
    if date:
        attendances = attendances.filter(date=date)

    # Prepare attendance data for JSON response
    data = {
        'attendances': [
            {
                'employee_name': attendance.employee.name,
                'employee_id': attendance.employee.emp_id,
                'status': attendance.status,
                'check_in': attendance.check_in.strftime('%H:%M:%S') if attendance.check_in else '',
                'check_out': attendance.check_out.strftime('%H:%M:%S') if attendance.check_out else '',
                'date': attendance.date.strftime('%Y-%m-%d')
            } for attendance in attendances
        ]
    }
    return JsonResponse(data)