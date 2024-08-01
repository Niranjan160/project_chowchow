import django_filters
from students.models import Student, Fees_detail

class Student_filter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = [
            'name', 'course', 'register_no',
            'academic_end_year','academic_start_year',
        ]


class Fees_details_filter(django_filters.FilterSet):
    class Meta:
        model = Fees_detail
        fields = [
            'reference_id', 'student_id__register_no', 'type_of_fees',
            'receipt_status', 'semester_number', 'receipt_submitted_date',
            'paid_date', 'student_id__course'
        ]