from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


from .models import StudentProfile
from django.db import IntegrityError




def home_view(request):
    return render(request, 'home.html')



from django.contrib.auth.models import User



def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        id_number = request.POST.get("id_number")

        # Validate ID number
        if not id_number.isdigit():
            messages.error(request, "ID Number must contain only digits")
            return redirect("register")

        if "@" not in email or "." not in email:
            messages.error(request, "Enter a valid email address")
            return redirect("register")

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name,
                last_name=surname
            )

            profile = StudentProfile.objects.get(user=user)
            profile.id_number = id_number
            profile.save()  # student_id already generated
            messages.success(request, f"Registration successful! Your Student ID is {profile.student_id}. You can now log in.")
            return redirect("login")

        except IntegrityError:
            messages.error(request, "Username or ID number already exists. Please try again.")
            return redirect("register")

    return render(request, "register.html")



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')  # Redirect to welcome page first
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required
# def welcome_view(request):
#     enrollments = Enrollment.objects.filter(student=request.user).select_related("course")
#     return render(request, "welcome.html", {"enrollments": enrollments})
#     # return render(request, 'welcome.html')


# @login_required
# def welcome(request):
#     # Retrieve all courses
#     courses = Course.objects.all()
#     # Retrieve courses the student is enrolled in
#     enrollments = Enrollment.objects.filter(user=request.user)
    
#     context = {
#         'courses': courses,
#         'enrollments': enrollments,
#     }
#     return render(request, 'welcome.html', context)
@login_required
def welcome_view(request):
    courses = Course.objects.all()
    # enrollments = Enrollment.objects.filter(user=request.user)
    enrollments = Enrollment.objects.filter(student=request.user)

    return render(request, 'welcome.html', {
        'courses': courses,
        'enrollments': enrollments,
    })

@login_required
def dashboard_view(request):
        # Fetch all courses (admin-created)
    courses = Course.objects.all()

    enrollments = Enrollment.objects.filter(student=request.user).select_related("course")
    # return render(request, "dashboard.html", {"enrollments": enrollments})
    # return render(request, 'dashboard.html')
    return render(request, "/dashboard.html", {
        "courses": courses,
        "enrollments": enrollments,
    })





from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# 


@login_required
def pay_course(request, course_id):
    # Pass banking details to template
    course = get_object_or_404(Course, id=course_id)
    banking_details = {
        'bank_name': 'FNB Bank',
        'account_name': 'SA HLOLO ENTLE HOLDINGS (PTY) LTD',
        'account_number': '6234567890',
        'branch_code': '632005',
        'reference': f'StudentID-{request.user.studentprofile.student_id}',
    }
    return render(request, 'pay_course.html', {'banking': banking_details, 'course': course})





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Enrollment, Course,Module



@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Enroll the student if not already enrolled
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('welcome')





@login_required
def enrolled_courses(request):
    # Get all courses the logged-in student is enrolled in
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    return render(request, 'enrolled_courses.html', {
        'enrollments': enrollments
    })














@login_required
def course_modules(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Only allow access if enrolled
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    if not is_enrolled:
        return render(request, "error.html", {"message": "You are not enrolled in this course."})
    modules = course.modules.all()  # grouped in template
    return render(request, "course_modules.html", {"course": course, "modules": modules})






@login_required
def paid_courses(request):
    # Get only courses the student has paid for
    enrollments = Enrollment.objects.filter(student=request.user, is_paid=True).select_related('course')
    
    return render(request, 'paid_courses.html', {
        'enrollments': enrollments
    })

    

@login_required
def unpaid_courses(request):
    # Get only courses the student has not paid for
    enrollments = Enrollment.objects.filter(student=request.user, is_paid=False).select_related('course')
    
    return render(request, 'unpaid_courses.html', {
        'enrollments': enrollments
    })



def my_assignments(request):
    # Get all courses the user is enrolled in
    enrollments = Enrollment.objects.filter(student=request.user)
    modules = Module.objects.filter(course__in=[en.course for en in enrollments])

    context = {
        'modules': modules
    }
    return render(request, 'my_assignments.html', context)


from django.shortcuts import render
from .models import Enrollment, ModuleProgress

def student_progress(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    progress_data = []

    for enrollment in enrollments:
        course = enrollment.course
        modules = course.modules.all()
        total_modules = modules.count()
        completed_modules = ModuleProgress.objects.filter(
            student=request.user, 
            module__in=modules, 
            is_completed=True
        ).count()

        progress_percent = (completed_modules / total_modules * 100) if total_modules else 0

        progress_data.append({
            'course': course,
            'completed_modules': completed_modules,
            'total_modules': total_modules,
            'progress_percent': progress_percent,  # make sure this exists!
        })

    return render(request, 'student_progress.html', {'progress_data': progress_data})

def all_courses(request):
    courses = Course.objects.all()
    return render(request, 'accounts/all_courses.html', {'courses': courses})


