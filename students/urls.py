from django.urls import path
from . import views


urlpatterns = [
    path("", views.student_dashboard, name="student_dashboard"),
    path("login/", views.loginPage, name="login_page"),
    path("logout/", views.logoutPage, name="logout_page"),
    path('register/', views.register_student, name="register_page"),

    path("officeadmin/", views.admin_dashboard, name="admin_dashboard"),
    path("officeadmin/studentdetails", views.admin_dashboard_student_details, name="admin_dashboard_student_details"),
    path("officeadmin/pendingdetails", views.pending_receipt_details, name="admin_dashboard_pending_details"),
    path("officeadmin/updatefeesdetail", views.update_fees_receipt_status, name="update_fees_receipt_status"),
    path("officeadmin/studentdetails/<int:register_no>", views.student_detailview, name="student_detail_view"),

    path('export-students/', views.export_students_to_excel, name='export_students'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
]
