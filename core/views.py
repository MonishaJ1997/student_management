from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Batch, Attendance, Marks, Exam
from .forms import AttendanceForm, MarksForm

def is_teacher(user):
    return user.is_authenticated and getattr(user, 'role', None) == 'teacher'

def is_parent(user):
    return user.is_authenticated and getattr(user, 'role', None) == 'parent'

@login_required
def dashboard(request):
    # simple dashboard, show counts
    students = Student.objects.count()
    exams = Exam.objects.count()
    return render(request, 'core/dashboard.html', {'students': students, 'exams': exams})

@login_required
def students_list(request):
    students = Student.objects.select_related('user').all()
    return render(request, 'core/students_list.html', {'students': students})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollment_set.select_related('batch').all()
    marks = student.marks_set.select_related('exam').all()
    attendance_records = student.attendance_set.order_by('-date')[:30]
    return render(request, 'core/student_detail.html', {'student': student, 'enrollments': enrollments, 'marks': marks, 'attendance_records': attendance_records})

# Teacher marks attendance
@user_passes_test(is_teacher)
def attendance_mark(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            return redirect('core:attendance_mark')
    else:
        form = AttendanceForm()
    # optional: show today's attendance for batch
    return render(request, 'core/attendance_mark.html', {'form': form})

# Teacher enter marks
@user_passes_test(is_teacher)
def marks_entry(request):
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.graded_by = request.user
            m.save()
            return redirect('core:marks_entry')
    else:
        form = MarksForm()
    return render(request, 'core/marks_entry.html', {'form': form})

# Parent dashboard showing their children and performance
@user_passes_test(is_parent)
def parent_dashboard(request, parent_id):
    if request.user.id != parent_id:
        # parents should access their own only (or add extra checks)
        return redirect('core:dashboard')
    children = request.user.children.all()  # related_name on Student.parent
    # gather data per child
    children_data = []
    for child in children:
        marks = child.marks_set.select_related('exam').all()
        attendance = child.attendance_set.order_by('-date')[:30]
        children_data.append({'child': child, 'marks': marks, 'attendance': attendance})
    return render(request, 'core/parent_view.html', {'children_data': children_data})
