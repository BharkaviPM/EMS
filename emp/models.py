from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Emp(models.Model):
    name = models.CharField(max_length=200)
    emp_id = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    working = models.BooleanField(default=True)
    department = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)  # Set your desired default value
    project = models.CharField(max_length=200, default='')  # Set a default project name
    meetings = models.IntegerField(default=0)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.name  # Optional: String representation of the model

# Attendance Model
class Attendance(models.Model):
    employee = models.ForeignKey(Emp, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Absent')

    def __str__(self):
        return f'{self.employee.name} - {self.date}'

# Performance Model
class Performance(models.Model):
    employee = models.ForeignKey(Emp, on_delete=models.CASCADE)
    attendance_score = models.FloatField(default=0)
    project_score = models.FloatField(default=0)
    publication_score = models.FloatField(default=0)
    meeting_score = models.FloatField(default=0)
    overtime_score = models.FloatField(default=0)
    total_score = models.FloatField(default=0)

    def calculate_overall_score(self):
        # Weights
        attendance_weight = 1
        project_weight = 5
        publication_weight = 3
        meeting_weight = 1
        overtime_weight = 0.5

        # Calculate the overall score as weighted sum
        self.total_score = (
            (self.attendance_score * attendance_weight) +
            (self.project_score * project_weight) +
            (self.publication_score * publication_weight) +
            (self.meeting_score * meeting_weight) +
            (self.overtime_score * overtime_weight)
        )
        self.save()

    def update_performance(self, attendance_score, project_score, publication_score, meeting_score, overtime_score):
        # Update the scores
        self.attendance_score = attendance_score
        self.project_score = project_score
        self.publication_score = publication_score
        self.meeting_score = meeting_score
        self.overtime_score = overtime_score

        # Recalculate the overall score after updating individual scores
        self.calculate_overall_score()

    def __str__(self):
        return f"{self.employee.name} - Total Score: {self.total_score}"

    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.question