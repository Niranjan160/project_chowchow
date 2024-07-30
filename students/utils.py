from django.core.mail import send_mail
from django.conf import settings

def send_reject_email(name, register_no, email):
    subject = "Regarding fees receipt"
    message = f"Hi {name}({register_no}), Your receipt is not valid. Please reupload the receipt and the details."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    print("Mail sent successfully")


# import pandas as pd
# from django.http import HttpResponse
# from .models import Student

# def export_students_to_excel(request):
#     # Get all students
#     students = Student.objects.all()

#     # Create a DataFrame
#     student_data = []
#     for student in students:
#         student_data.append({
#             'Email': student.user.email,
#             'Academic Year': student.academic_year,
#             'Current Semester': student.current_semester
#         })

#     df = pd.DataFrame(student_data)

#     # Create an HttpResponse object with the appropriate Excel header.
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=students.xlsx'

#     # Use pandas to create an Excel writer object and write the DataFrame to it.
#     with pd.ExcelWriter(response, engine='openpyxl') as writer:
#         df.to_excel(writer, sheet_name='Students', index=False)

#     return response
