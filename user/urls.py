from django.urls import path
from .views import *
urlpatterns=[
path('driver_registration/',driver_registration,name='driver_registration'),
path('',home,name='home'),
path('login/',signin,name='signin'),
path('user_dashboard/',user_dashboard,name='user_dashboard'),
path('report/<int:lic>/',user_report,name='user_report'),
path('user_pending_fine/<int:lic>/',user_pending_fine,name='user_pending_fine'),
path('pending_fine_table/',pending_fine_table,name='pending_fine_table'),
path('pending_fine_view_modal/',pending_fine_view_modal,name='pending_fine_view_modal'),
path('user_paid_fine/<int:lic>/',user_paid_fine,name='user_paid_fine'),
path('paid_fine_table/',paid_fine_table,name='paid_fine_table'),
path('paid_fine_view_modal/',paid_fine_view_modal,name='paid_fine_view_modal'),
path('user_fine_tickets/<int:lic>/',user_fine_tickets,name='user_fine_tickets'),
path('fine_tickets_table/',fine_tickets_table,name='user_fine_tickets_table'),
path('forgot-password/',user_Forgot_Password,name='user_Forgot_Password'),
path('reset-password/',reset_password,name='reset_password'),
path('user_profile/<int:lic>/',user_profile,name='user_profile'),
path('profile_details/<int:lic>/',profile_details,name='user_profile_details'),
path('verification_code/',verification_code,name='verification_code'),
path('payments_process/<int:lic>/<int:ref>/',payments_process,name='payments_process'),
path('card_payment/<int:lic>/<int:ref>/',card_payment,name='card_payment'),
path('payments_thankyou/<int:lic>/',payments_thankyou,name='payments_thankyou'),
path('user_logout/',user_logout,name='user_logout'),



]
