from django.urls import path
from .views import *

urlpatterns=[
    path('police_login/',police_login,name='police_login'),
    path('',police_home,name='police_home'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('tpo-reset-password/',tpo_reset_password,name='tpo_reset_password'),
    path('police_dashboard/<int:pid>/',police_dashboard,name='police_dashboard'),
    path('add_new_fine/<int:pid>/',add_new_fine,name='add_new_fine'),
    path('check_revenue_license/<int:pid>/',check_revenue_license,name='check_revenue_license'),
    path('view_reported_fine/<int:pid>/',view_reported_fine,name='view_reported_fine'),
    path('view_reported_fine_table/',view_reported_fine_table,name='view_reported_fine_table'),
    path('police_profile/<int:pid>/',police_profile,name='police_profile'),
    path('profile_details/<int:pid>/',profile_details,name='profile_details'),
    path('verification_code/',verification_code,name='verification_code'),
    path('user-reported-issues/<int:pid>/',user_reported_issues,name='user_reported_issues'),
    path('tpo_logout/',tpo_logout,name='tpo_logout'),


]