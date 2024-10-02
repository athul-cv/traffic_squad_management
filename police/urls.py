from django.urls import path
from .views import *
urlpatterns=[
    path('dashboard/',dashboard,name='dashboard'),
    path('register/',register,name='reg'),
    path('Login/',signin,name='login'),
    path('LogOut/',signout,name='signout'),
    path('forgot/',forgot,name='forgotpass'),
    path('otp/',otp,name='otpverification'),
    path('',guest,name='guest'),
    path('admin/',admin,name='admin'),
    path('tpo/',tpo,name='tpo'),
    path('add_traffic_officer/',add_traffic_officer,name='add_traffic_officer'),
    path('view_all_traffic_officers/',view_all_traffic_officers,name='view_all_traffic_officers'),
    path('delete-officers/',delete_officers,name='delete_officers'),
    path('edit_traffic_officer/',edit_officers,name="edit_officers"),
    path('mtd_account/',mtd_account,name='mtd_account'),
    path('fine_tickets/',fine_tickets,name='fine_tickets'),
    path('edit_fine_tickets/',edit_fine_tickets,name='edit_fine_tickets'),
    path('delete_fine/',delete_fines,name='delete_fines'),
    path('view_drivers/',view_drivers,name='view_drivers'),
    path('delete-drivers/',delete_drivers,name='delete_drivers'),
    path('paid_fine_tickets/',paid_fine_tickets,name='paid_fine_tickets'),
    path('pending_fine_tickets/', pending_fine_tickets, name='pending_fine_tickets'),
    path('reported-issues/', reported_issues, name='reported_issues'),
    path('admin_signout/',admin_signout,name='police_logout'),

]
