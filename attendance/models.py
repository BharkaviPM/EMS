from django.db import models

# Create your models here.
# models.py
class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)  # True for present, False for absent

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {'Present' if self.status else 'Absent'}"

