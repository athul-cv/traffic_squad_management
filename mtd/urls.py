from django.urls import path
from.views import *
urlpatterns=[
 path('mtd-login/',mtd_login,name='mtd_login'),
 path('mtd_forgot_password/',mtd_forgot_password,name='mtd_forgot_password'),
 path('new_password/',new_password,name='new_password'),
 path('',mtd_home,name='mtd_home'),
 path('mtd_dashboard/',mtd_dashboard,name='mtd_dashboard'),
 path('add_driver/',add_driver,name='add_driver'),
 path('edit-driver/',edit_driver,name='edit_driver'),
 path('view_all_driver/',view_all_driver,name='view_all_driver'),
 path('delete-driver/', delete_drivers, name='delete_driver'),
 path('view_all_drivers_delete_modal/', view_all_drivers_delete_modal, name='view_all_drivers_delete'),
 path('mtd_profile/',mtd_profile,name='mtd_profile'),
 path('add_vehicle/',add_vehicle,name='add_vehicle'),
 path('verification_code/',verification_code,name='verification_code'),
 path('mtd_logout/',mtd_logout,name='mtd_logout'),
 ]