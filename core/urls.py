from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'core'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.students_list, name='students_list'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
    path('marks/entry/', views.marks_entry, name='marks_entry'),
    path('parent/<int:parent_id>/children/', views.parent_dashboard, name='parent_view'),
   


    # Login view
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Logout view
   path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),
]


