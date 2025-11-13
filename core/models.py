from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def is_teacher(self):
        return self.role == 'teacher'
    def is_student(self):
        return self.role == 'student'
    def is_parent(self):
        return self.role == 'parent'


from django.conf import settings
from django.db import models
from decimal import Decimal
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    phone = models.CharField(max_length=32, blank=True)
    department = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=32, unique=True)
    dob = models.DateField(null=True, blank=True)
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')  # parent is a User with role 'parent'

    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Batch(models.Model):
    """A class or batch (e.g., 10th A, Semester 1)"""
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    year = models.IntegerField(default=timezone.now().year)
    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return f"{self.name} ({self.course.code})"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'batch')

class Exam(models.Model):
    name = models.CharField(max_length=255)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.name} - {self.batch.name}"

class Attendance(models.Model):
    """One record per student per date per batch"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # usually teacher

    class Meta:
        unique_together = ('student','batch','date')

class Marks(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # teacher

    class Meta:
        unique_together = ('exam','student')
