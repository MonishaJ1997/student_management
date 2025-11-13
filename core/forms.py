from django import forms
from .models import Attendance, Marks

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student','batch','date','present']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['exam','student','marks_obtained']
