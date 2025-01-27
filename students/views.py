from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from students.models import Student, Fees_detail
from students.forms import fees_details_form, CustomUserCreationForm, StudentForm, ExcelUploadForm
from datetime import date
# from django.core.paginator import Paginator
from students.utils import send_reject_email
import pandas as pd
from students.filters import Student_filter, Fees_details_filter
from datetime import timedelta
from django.utils import timezone
import openpyxl


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    else:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_student:
                    return redirect("student_dashboard")
                elif user.is_office_admin:
                    return redirect("admin_dashboard")
            else:
                return render(request, "students/login.html", {
                    "message": "Invalid email or password."
                })
        else:
            return render(request, "students/login.html")


def logoutPage(request):
    logout(request)
    return redirect("login_page")


# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('dashboardpage')
#     else:
#         context = {}
#         context['form'] = createUserForm()
#         if request.method == 'POST':
#             context['form'] = createUserForm(request.POST)
#         if context['form'].is_valid():
#             context['form'].save()
#             return redirect('login')

#         return render(request, 'appone/register.html', context)

def register_student(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    else:   
        if request.method == 'POST':
            user_form = CustomUserCreationForm(request.POST)
            student_form = StudentForm(request.POST)
            print("working")
            print(user_form.is_valid())
            print(student_form.errors)
            if user_form.is_valid() and student_form.is_valid():
                user = user_form.save(commit=False)
                user.save()
                print("s2 working")
                student = student_form.save(commit=False)
                print(user)
                student.Student = user
                student.email = user.email
                student.save()

                return redirect('login_page')  # Redirect to login or any other page after successful registration
        else:
            user_form = CustomUserCreationForm()
            student_form = StudentForm()

        return render(request, 'students/student_register_page.html', {
            'user_form': user_form,
            'student_form': student_form
        })

@login_required
def student_dashboard(request):
    if request.user.is_office_admin(): 
        return redirect("admin_dashboard")
    context = {}
    context["form"] = fees_details_form()
    context["student"] = Student.objects.get(Student=request.user)
    context["fees_history"] = Fees_detail.objects.filter(student_id=context["student"])
    if request.method == "POST":
        fees_details = fees_details_form(request.POST, request.FILES)
        if fees_details.is_valid():
            fees_details = fees_details.save(commit=False)
            fees_details.student_id = context["student"]
            fees_details.save()
    return render(request, 'students/student_dashboard.html', context=context)


@login_required
def admin_dashboard(request):
    if request.user.is_student():
       return redirect("student_dashboard")
    context = {}
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    context["students_count"] = Student.objects.filter(
        academic_end_year__year__gte=date.today().year
    ).count()
    context["uploaded_count"] = Fees_detail.objects.filter(receipt_submitted_date__gte=thirty_days_ago).count()
    context["verified_count"] = Fees_detail.objects.filter(receipt_submitted_date__gte=thirty_days_ago, receipt_status="ACC").count()
    context["pending_count"] = Fees_detail.objects.filter(receipt_submitted_date__gte=thirty_days_ago,receipt_status="PEN").count()
    context["fees_details"] =  Fees_detail.objects.filter(receipt_status="PEN").order_by("-receipt_submitted_date")

    return render(request, 'students/admin_dashboard.html', context)

@login_required
def pending_receipt_details(request):
    context = {}
    # pending_fees_list = Fees_detail.objects.filter(receipt_status="PEN").order_by("-receipt_submitted_date")
    # paginator = Paginator(pending_fees_list, 20)
    # page_number = request.GET.get("page") or 1
    # context["page_obj"] = paginator.get_page(page_number)
    context["fees_details"] = Fees_details_filter(request.GET, Fees_detail.objects.all().order_by("-receipt_submitted_date"))
    
    return render(request, "students/admin_pending_details.html", context)

@login_required
def update_fees_receipt_status(request):
    # Need to add exception
    if request.method == "POST":
        status = request.POST["receipt_status"]
        reference_id = request.POST["reference_id"]
        # print(status, reference_id)
        student = Fees_detail.objects.get(reference_id=reference_id).student_id
        status_return = "Accepted"
        if status == "REJ":
            status_return = "Rejected"
            send_reject_email(student.name, student.register_no, student.email)
        fees_detail = Fees_detail.objects.get(reference_id=reference_id)
        fees_detail.receipt_status = status
        fees_detail.save()
        return HttpResponse(f"{status_return}") # uodate it to jsonResponse
    else: 
        return HttpResponseBadRequest("Not like this :)")

@login_required
def admin_dashboard_student_details(request):
    if request.user.is_student():
       return redirect("student_dashboard")
    context = {}
    context["students_details"] = Student_filter(request.GET, queryset=Student.objects.filter(
        academic_end_year__year__gte=date.today().year
    ).order_by('register_no'))
    # students_details = Student.objects.filter(
    #     academic_end_year__year__gte=date.today().year
    # ).order_by('register_no')
    # paginator = Paginator(students_details, 30)
    # page_number = request.GET.get("page") or 1
    # context["page_obj"] = paginator.get_page(page_number)
    return render(request, 'students/admin_dashboard_student_details.html', context)

def export_students_to_excel(request):
    # Get all students
    students = Student.objects.all()

    # Create a DataFrame
    student_data = []
    for student in students:
        sd = vars(student)
        sd.pop('_state')
        student_data.append(sd)

    df = pd.DataFrame(student_data)

    # Create an HttpResponse object with the appropriate Excel header.
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=students.xlsx'

    # Use pandas to create an Excel writer object and write the DataFrame to it.
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Students', index=False)

    return response


def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active

            for row in ws.iter_rows(min_row=2):  # Assuming first row is header
                email = row[0].value
                user_type = row[1].value
                academic_year = row[2].value
                profile_photo = row[3].value
                course = row[4].value

                # Create or update student record
                user, created = Student.objects.get_or_create(email=email, defaults={'user_type': user_type})
                Student.objects.update_or_create(user=user, defaults={
                    'academic_year': academic_year,
                    'profile_photo': profile_photo,
                    'course': course,
                })
            # messages.success(request, "Students have been added/updated successfully")
            return redirect("upload_excel")
    else:
        form = ExcelUploadForm()

    return render(request, "upload_excel.html", {"form": form})

@login_required
def student_detailview(request,register_no):
    context = {}
    context["student"] = Student.objects.get(register_no=register_no)
    context["fees_history"] = Fees_detail.objects.filter(student_id=context["student"])
    return render(request, 'students/student_detailview.html', context=context)
