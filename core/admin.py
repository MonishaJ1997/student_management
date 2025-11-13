from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Teacher, Student, Course, Batch, Enrollment, Exam, Attendance, Marks

User = get_user_model()  # ✅ Returns the actual User model class

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

# Register other models
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Enrollment)
admin.site.register(Exam)
admin.site.register(Attendance)
admin.site.register(Marks)
