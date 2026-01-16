

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # <-- Home page
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('register/', views.register, name='register'),

    path('welcome/', views.welcome_view, name='welcome'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    path('pay-course/<int:course_id>/', views.pay_course, name='pay_course'),
    path('paid-courses/', views.paid_courses, name='paid_courses'),
    path('unpaid-courses/', views.unpaid_courses, name='unpaid_courses'),
    # path('enrolled-courses/', views.enrolled_courses, name='enrolled_courses'),  # new
    path('enrolled-courses/', views.welcome_view, name='enrolled_courses'),


   
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),  # enroll a specif
    path('my-assignments/', views.my_assignments, name='my_assignments'),
    path('progress/', views.student_progress, name='student_progress'),
    path('courses/', views.all_courses, name='all_courses'),
    # accounts/urls.py
    path('course/<int:course_id>/modules/', views.course_modules, name='course_modules'),

   


]
