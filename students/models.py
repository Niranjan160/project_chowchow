from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.utils import timezone


course_choices = (
    ("MSC CSE", "Master of Science Computer Science and Engineering"),
    ("MSC DS", "Master of Science Data Science"),
    ("MSC AI", "Master of Science Artificial Intelligence"),
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
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default="S")
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


def student_profile_image_directory(instance, filename):
    ext = filename.split('.')[-1]
    # path = profile_images/<reg_no>.<img_extension>
    return "profile_images{0}.{1}".format(
        instance.register_no,
        ext,
    )

class Student(models.Model):

    Student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": "S"}
    )
    profile_photo = models.FileField(
        upload_to=student_profile_image_directory,
        default="default-avatar.png",
        null=True,
        blank=True
    )
    register_no = models.CharField(
        primary_key=True, 
        max_length=30
    )
    name = models.CharField(
        max_length=100
    )
    date_of_birth = models.DateField()
    email = models.EmailField(
        unique=True, 
        validators=[

        ]
    )
    phone_number = models.PositiveIntegerField()
    course = models.CharField(
        max_length=50,
        choices=course_choices
    )
    academic_start_year = models.DateField(blank=True, null=True)
    academic_end_year = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return f"{self.register_no} - {self.name}"

    # def clean(self) -> None:
    #     super().clean()
    #     if self.Student.email != self.email:
    #         raise ValidationError({"Email does not getting matched"})

    @property
    def current_semester(self):
        if not self.academic_start_year or not self.academic_end_year:
            return None
        total_months = (self.academic_end_year.year - self.academic_start_year.year) * 12 + (self.academic_end_year.month - self.academic_start_year.month)
        months_per_semester = total_months / 6
        months_since_start = (timezone.now().year - self.academic_start_year.year) * 12 + (timezone.now().month - self.academic_start_year.month)
        current_semester = (months_since_start // months_per_semester) + 1
        return int(current_semester)

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
    return "fees_receipts/{0}/{1}/{2}/semester_{3}/{4}-{5}.{6}".format(
        date.today().year,
        instance.type_of_fees,
        instance.student_id.course,
        instance.semester_number,
        instance.student_id.register_no,
        instance.reference_id,
        ext,
    )


class Fees_detail(models.Model):
    reference_id = models.CharField(
        primary_key=True,
        max_length=30
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
        choices=receipt_status_choices,
        default="PEN"
    )
    fees_receipt = models.FileField(
        upload_to=student_fees_directory,
        default=None,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.student_id} - {self.reference_id} - {self.type_of_fees}"