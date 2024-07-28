from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from students.models import Student, Fees_detail
from students.forms import fees_details_form
from datetime import date
from django.core.paginator import Paginator

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

