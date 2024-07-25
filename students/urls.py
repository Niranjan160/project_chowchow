from django.urls import path
from . import views


urlpatterns = [
    path("", views.student_dashboard, name="student_dashboard"),
    path("officeadmin/", views.admin_dashboard, name="admin_dashboard"),
    path("login/", views.loginPage, name="login_page"),
    path("logout/", views.logoutPage, name="logout_page"),
]
