from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date


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

    Student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": "S"}
    )
    register_no = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.PositiveIntegerField()
    type_of_degree = models.CharField(max_length=5,choices=degree_choices) #Require validator function
    type_of_department = models.CharField(max_length=5,choices=department_choices)

    def __str__(self) -> str:
        return f"{self.register_no} - {self.name}"


fees_choices = (
("SF", "Semester Fees"),
("EF", "Exam Fees"),
)
receipt_status_choices = (
("PEN", "Pending"),
("ACC", "Accepted"),
("REJ", "Rejected"),
)

def student_fees_directory(instance, filename):
    ext = filename.split('.')[-1]
    # path = fees_receipt/2024/EF/MSC/<dept?>/S1/<reg_no>.pdf
    return "fees_receipts/{0}/{1}/{2}/{3}/semester_{4}/{5}.{6}".format(
        date.today().year,
        instance.type_of_fees,
        instance.student_id.type_of_degree,
        (instance.student_id.type_of_department or ""),
        instance.semester_number,
        instance.student_id.register_no,
        ext,
    )


class Fees_detail(models.Model):
    reference_id = models.IntegerField(
        primary_key=True
    )
    student_id = models.ForeignKey(
        "Student", 
        on_delete=models.CASCADE
    )
    type_of_fees = models.CharField(
        max_length=5,
        choices=fees_choices
    )
    paid_date = models.DateField()
    fees_amount = models.PositiveIntegerField()
    semester_number = models.PositiveIntegerField(
        validators= [
            MaxValueValidator(12),
            MinValueValidator(1)
        ],
        default=1
    )
    receipt_submitted_date = models.DateField(
        auto_now_add=True
    )
    receipt_status = models.CharField(
        max_length=5,
        choices=receipt_status_choices
    )
    fees_receipt = models.FileField(
        upload_to=student_fees_directory,
        default=None,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.student_id} - {self.reference_id} - {self.type_of_fees}"