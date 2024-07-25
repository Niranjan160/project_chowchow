from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

department_choices = (
    ("CSE", "Computer Science and Engineering"),
    ("DS", "Data Science"),
    ("AI", "Artificial Intelligence"),
)
degree_choices = (
    ("MSC", "Master of Science"),
    ("MCA", "Master of Computer Application"),
    ("MTECH", "Master of Technology"),
)
fees_choices = (
    ("SF", "Semester Fees"),
    ("EF", "Exam Fees"),
)
receipt_status_choices = (
    ("PEN", "Pending"),
    ("ACC", "Accepted"),
    ("REJ", "Rejected"),
)

class User(AbstractUser):

    ROLE_CHOICES = (
        ('OA', 'Office Administrator'),
        ('S', 'Student'),
    )
    username = None
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default="Student")
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def is_office_admin(self):
        return self.role == 'OA'

    def is_student(self):
        return self.role == 'S'

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.email

class Student(models.Model):
    Student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    register_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField()
    type_of_degree = models.CharField(max_length=5,choices=degree_choices) #Require validator function
    type_of_department = models.CharField(max_length=5,choices=department_choices)

    def __str__(self) -> str:
        return f"{self.register_no} - {self.name}"


class Fees_detail(models.Model):
    reference_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey("Student", on_delete=models.CASCADE)
    type_of_fees = models.CharField(max_length=5,choices=fees_choices)
    paid_date = models.DateField()
    receipt_submitted_date = models.DateField(auto_now_add=True)
    receipt_status = models.CharField(max_length=5,choices=receipt_status_choices)

    def __str__(self) -> str:
        return f"{self.student_id} - {self.reference_id} - {self.type_of_fees}"