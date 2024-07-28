from django.urls import path
from . import views


urlpatterns = [
    path("", views.student_dashboard, name="student_dashboard"),
    path("login/", views.loginPage, name="login_page"),
    path("logout/", views.logoutPage, name="logout_page"),
    path("officeadmin/", views.admin_dashboard, name="admin_dashboard"),
    path("officeadmin/studentdetails", views.admin_dashboard_student_details, name="admin_dashboard_student_details"),
    path("officeadmin/pendingdetails", views.pending_receipt_details, name="admin_dashboard_pending_details"),
]
