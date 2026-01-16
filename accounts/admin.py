# from django.contrib import admin

# Register your models here.

# from django.contrib import admin
# from .models import StudentProfile
# from django.contrib.auth.models import User

# # Option 1: Register StudentProfile with student_id visible
# class StudentProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'student_id', 'id_number')  # Fields to show in admin list
#     search_fields = ('user__username', 'student_id', 'user__first_name', 'user__last_name')

# admin.site.register(StudentProfile, StudentProfileAdmin)


# accounts/admin.py
from django.contrib import admin
from .models import Course, Enrollment, Module


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "saqa_id", "nqf_level", "credit", "fee")
    inlines = [ModuleInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "is_paid", "date_enrolled")
    list_filter = ("course", "is_paid")

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("course", "module_type", "order", "code", "title", "nqf_level", "credits")
    list_filter = ("course", "module_type")
    search_fields = ("code", "title")







# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ("name",)

# @admin.register(Assignment)
# class AssignmentAdmin(admin.ModelAdmin):
#     list_display = ("title", "course", "due_date", "uploaded_at")
#     list_filter = ("course", "due_date")
#     search_fields = ("title", "course__name")
