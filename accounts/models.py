from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    id_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            while True:
                new_id = random.choice(string.ascii_uppercase) + str(random.randint(100, 999))
                if not StudentProfile.objects.filter(student_id=new_id).exists():
                    self.student_id = new_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.student_id})"

# Signal to create StudentProfile automatically
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        profile = StudentProfile.objects.create(user=instance)
        profile.save()  # This triggers save() and generates student_id




# class Course(models.Model):
#     saqa_id = models.CharField(max_length=10)
#     name = models.CharField(max_length=100)
#     nqf_level = models.IntegerField()
#     credit = models.IntegerField()
#     fee = models.DecimalField(max_digits=10, decimal_places=2)  # optional

#     def __str__(self):
#         return self.name

# class Enrollment(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     is_paid = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.student.username} - {self.course.name}"

class Course(models.Model):
    saqa_id   = models.CharField(max_length=20)
    name      = models.CharField(max_length=200)
    nqf_level = models.PositiveIntegerField(default=5)
    credit    = models.PositiveIntegerField(default=0)
    fee       = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} (SAQA {self.saqa_id})"

# class Course(models.Model):
#     name = models.CharField(max_length=255)
#     saqa_id = models.CharField(max_length=50, blank=True, null=True)
#     nqf_level = models.IntegerField(default=1)
#     credit = models.IntegerField(default=0)

#     def __str__(self):
#         return self.name



class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.username} → {self.course.name}"


# class Module(models.Model):
#     MODULE_TYPES = [
#         ("KM", "Knowledge Module"),
#         ("PM", "Practical Skills Module"),
#         ("WM", "Work Experience Module"),
#     ]
#     course      = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
#     code        = models.CharField(max_length=50)
#     title       = models.CharField(max_length=255)
#     nqf_level   = models.PositiveIntegerField(default=5)
#     credits     = models.PositiveIntegerField(default=0)
#     module_type = models.CharField(max_length=2, choices=MODULE_TYPES, default="KM")
#     order       = models.PositiveIntegerField(default=0)

#     class Meta:
#         ordering = ["module_type", "order"]
#         unique_together = ("course", "code")

#     def __str__(self):
#         return f"{self.code} - {self.title}"



class Module(models.Model):
    MODULE_TYPES = [
        ("KM", "Knowledge Module"),
        ("PM", "Practical Skills Module"),
        ("WM", "Work Experience Module"),
    ]
    course      = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    code        = models.CharField(max_length=50)
    title       = models.CharField(max_length=255)
    nqf_level   = models.PositiveIntegerField(default=5)
    credits     = models.PositiveIntegerField(default=0)
    module_type = models.CharField(max_length=2, choices=MODULE_TYPES, default="KM")
    order       = models.PositiveIntegerField(default=0)

    # New assessment fields
    formative_assessment = models.FileField(
        upload_to="module_assessments/formative/", 
        blank=True, 
        null=True
    )
    summative_assessment = models.FileField(
        upload_to="module_assessments/summative/", 
        blank=True, 
        null=True
    )

    class Meta:
        ordering = ["module_type", "order"]
        unique_together = ("course", "code")

    def __str__(self):
        return f"{self.code} - {self.title}"


# class Course(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class Assignment(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     file = models.FileField(upload_to="assignments/")
#     due_date = models.DateField()
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.course.name}"


from django.conf import settings

class ModuleProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "module")

    def __str__(self):
        return f"{self.student.username} - {self.module.title} - {'Completed' if self.is_completed else 'Pending'}"
