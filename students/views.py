from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from students.models import Student, Fees_detail
from students.forms import fees_details_form, CustomUserCreationForm, StudentForm
from datetime import date
from django.core.paginator import Paginator
from students.utils import send_reject_email
import pandas as pd

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
            if user_form.is_valid() and student_form.is_valid():
                user = user_form.save(commit=False)
                user.save()

                student = student_form.save(commit=False)
                print(user)
                student.student_id = user
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
    context["students_count"] = Student.objects.filter(
        academic_end_year__year__gte=date.today().year
    ).count()
    return render(request, 'students/admin_dashboard.html', context)

@login_required
def pending_receipt_details(request):
    context = {}
    pending_fees_list = Fees_detail.objects.filter(receipt_status="PEN").order_by("-receipt_submitted_date")
    paginator = Paginator(pending_fees_list, 20)
    page_number = request.GET.get("page") or 1
    context["page_obj"] = paginator.get_page(page_number)
    return render(request, "students/admin_pending_details.html", context)

@login_required
def update_fees_receipt_status(request):
    # Need to add exception
    print("working")
    if request.method == "POST":
        status = request.POST["receipt_status"]
        reference_id = request.POST["reference_id"]
        print(status, reference_id)
        student = Fees_detail.objects.get(reference_id=reference_id).student_id
        if status == "REJ":
            send_reject_email(student.name, student.register_no, student.email)
        fees_detail = Fees_detail.objects.get(reference_id=reference_id)
        fees_detail.receipt_status = status
        fees_detail.save()
        return redirect('admin_dashboard_student_details') # uodate it to jsonResponse
    else: 
        return HttpResponseBadRequest("Not like this :)")

@login_required
def admin_dashboard_student_details(request):
    if request.user.is_student():
       return redirect("student_dashboard")
    context = {}
    students_details = Student.objects.filter(
        academic_end_year__year__gte=date.today().year
    ).order_by('register_no')
    paginator = Paginator(students_details, 30)
    page_number = request.GET.get("page") or 1
    context["page_obj"] = paginator.get_page(page_number)
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