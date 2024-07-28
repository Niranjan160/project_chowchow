from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from students.models import Student
# Create your views here.


@login_required
def student_dashboard(request):
    if request.user.is_office_admin(): 
        return redirect("admin_dashboard")
    context = {}
    if request.method == "GET":
        context["student"] = Student.objects.get(Student=request.user)
    elif request.method == "POST":
        pass
    return render(request, 'students/student_dashboard.html', context=context)

@login_required
def admin_dashboard(request):
    if request.user.is_student():
       return redirect("student_dashboard")
    return render(request, 'students/admin_dashboard.html')


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
