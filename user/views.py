from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Driver_registration, Reporting
from tpo.models import IssueFine
from django.contrib.auth import authenticate, logout, login
from police.models import *
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def driver_registration(request):
    if request.method == 'POST':
        LicenseID = request.POST.get('id')
        DriverEmail = request.POST.get('email')
        Driverpassword = request.POST.get('driverpassword')
        Driverconfirmpassword = request.POST.get('driverpasswordconfirm')
        Drivername = request.POST.get('name')
        licenseissuedate = request.POST.get('licenseissuedate')
        licenseexpiredate = request.POST.get('licenseexpiredate')
        registereddate = request.POST.get('registereddate')
        licenseissuedate = datetime.strptime(licenseissuedate,"%Y-%m-%d")
        licenseexpiredate = datetime.strptime(licenseexpiredate,"%Y-%m-%d")
        print(type(licenseexpiredate))
        print(LicenseID, DriverEmail, Drivername, licenseissuedate,licenseexpiredate)
        if Driverpassword == Driverconfirmpassword:
            if Driver_registration.objects.filter(driver_email=DriverEmail).exists():
                messages.warning(request, 'email exists')
            elif Driver_registration.objects.filter(license_id=LicenseID ).exists():
                messages.warning(request, 'id exists')
            elif licenseissuedate >= licenseexpiredate:
                messages.warning(request,'expiration date must be after the issue date')
            elif licenseexpiredate <= datetime.now():
                messages.warning(request,"license expiration date can't be in the past")
            else:
                add_driver = Driver_registration.objects.create(license_id=LicenseID, driver_email=DriverEmail,
                                                                driver_password=Driverpassword,
                                                                driver_name=Drivername, license_issue_date=licenseissuedate,
                                                                license_expire_date=licenseexpiredate,
                                                                registered_at=registereddate)
                add_driver.save()
                print('driver_added')
        else:
            messages.warning(request, 'password mismatch')
    return render(request, 'Driver_registration.html')

def signin(request):
    if request.method == 'POST':
        lic = request.POST.get('license_id')
        password = request.POST.get('driver_password')
        if Driver_registration.objects.filter(license_id=lic,driver_password=password).exists():
            request.session['id']=lic
            return redirect(user_dashboard)
        else:
            messages.warning(request,"Account Not Found!")
    return render(request,'login.html')


def user_dashboard(request):
    paid = 0
    unpaid = 0
    paid_fee = 0
    unpaid_fee = 0
    lic = request.session.get('id')
    print(lic)
    driver = Driver_registration.objects.get(license_id=lic)
    fines = IssueFine.objects.filter(license_id=lic)
    for f in fines:
        if f.status == 'pending':
            unpaid+=1
            unpaid_fee+=f.total_amount
        else:
            paid+=1
            paid_fee += f.total_amount
    return render(request,'user_dashboard.html',{'lic':lic,'d':driver,'paid':paid,'unpaid':unpaid,'paid_fee':paid_fee,'unpaid_fee':unpaid_fee})

def user_pending_fine(request,lic):
    print(lic)
    fine = IssueFine.objects.filter(license_id=lic,status="pending")
    # for f in fine:
    #     if f.status == "pending":
    #         fine = IssueFine.objects.filter(status="pending")
    return render(request,'user_pending_fine.html',{'fine':fine,'lic':lic})

def pending_fine_table(request):
    return render(request,'pending_fine_table.html')

def pending_fine_view_modal(request):
    return render(request,'pending_fine_view_modal.html')


def user_paid_fine(request,lic):
    fine = IssueFine.objects.filter(license_id=lic)
    return render(request,'user_paid_fine.html',{'lic':lic,'f':fine})

def paid_fine_table(request):
    return render(request,'paid_fine_table.html')

def paid_fine_view_modal(request):
    return render(request,'paid_fine_view_modal.html')

def user_fine_tickets(request,lic):
    fines = Fine_tickets.objects.all()
    return render(request,'user_fine_tickets.html',{'lic':lic,'fines':fines})

def fine_tickets_table(request):
    return render(request,'fine_tickets_table.html')


def user_Forgot_Password(request):
    if request.method=="POST":
        email = request.POST.get("email")

        try:
            if Driver_registration.objects.get(driver_email=email):
                def generate_otp():
                    return random.randint(1000, 9999)

                otp = generate_otp()
                time = datetime.now()
                print('generated_otp', otp)
                # time.sleep(300)
                send_mail('forgot password', f'otp for your password reset:{otp}', settings.EMAIL_HOST_USER, [email])
                request.session['otp'] = otp
                request.session['username'] = email
                request.session['time'] = str(time)
                return redirect(reset_password)
        except:
            messages.warning(request, "Email doesn't exist")
    return render(request,'user_Forgot_Password.html')


def reset_password(request):
    otp=request.session.get('otp')
    user = request.session.get('username')
    time=request.session.get('time')
    send_time = datetime.strptime(time,"%Y-%m-%d %H:%M:%S.%f")
    print("ttt",send_time.hour,send_time.minute,send_time.second)
    end_time=datetime.now()
    diff = end_time-send_time
    print(diff)
    print(timedelta(minutes=5))
    if request.method == 'POST':
        confirm_otp=int(request.POST.get('otp'))
        print(confirm_otp,type(confirm_otp))
        newpass=request.POST.get('pass1')
        confirmpass=request.POST.get('pass2')
        print(newpass,confirmpass)
        if otp==confirm_otp and  newpass==confirmpass and diff <= timedelta(minutes=5):
            user=Driver_registration.objects.get(driver_email=user)
            user.driver_password=newpass
            user.save()
            return redirect(signin)
        elif otp!=confirm_otp:
            messages.error(request,'Invalid OTP')
        elif newpass!=confirmpass:
            messages.error(request,'Password Mismatch')
        elif otp==confirm_otp and diff >= timedelta(minutes=5):
            messages.error(request, "Time Exceeded!")

    return render(request, 'reset_password.html')

def home(request):
    return render(request,'home.html')

def user_profile(request,lic):
    driver = Driver_registration.objects.get(license_id=lic)
    if request.method == "POST":
        old = request.POST.get('oldpassword')
        new = request.POST.get('newpassword')
        confirm = request.POST.get('passwordconfirm')
        if new == confirm:
            if old == driver.driver_password:
                driver.driver_password=new
                driver.save()
                messages.success(request,"Password changed successfully!!")
            else:
                messages.error(request, "Current Password Incorrect!!")
        else:
            messages.error(request, "Password mismatch!!")
    return render(request,'user_profile.html',{'lic':lic,'d':driver})

def profile_details(request,lic):
    driver = Driver_registration.objects.get(license_id=lic)
    return render(request,'profile_details.html',{'lic':lic,'d':driver})

def verification_code(request):
    return render(request,'verification-code.html')

def payments_process(request,lic,ref):
    driver = Driver_registration.objects.get(license_id=lic)
    fine = IssueFine.objects.get(ref_no=ref)
    return render(request,'payments_process.html',{'lic':lic,'f':fine,'d':driver})

def card_payment(request,lic,ref):
    fine = IssueFine.objects.get(ref_no=ref)
    if request.method == 'POST':
        paid = request.POST.get('fine')
        print(paid)
        if paid == "paid":
        # print(fine.status)
            fine = IssueFine.objects.get(ref_no=ref)
            fine.status = paid
            fine.save()
            print('paidd')
            if fine.status == "paid":
                return redirect(payments_thankyou,lic)
    return render(request,'payment.html',{'lic':lic,'f':fine})

def payments_thankyou(request,lic):
    return render(request,'payments_thankyou.html',{'lic':lic})


def user_report(request,lic):
    if request.method == "POST":
        accident_type = request.POST.get("accident_type")
        accident_description = request.POST.get("accident_description")
        accident_location = request.POST.get("accident_location")
        accident_date = request.POST.get("accident_date")
        accident_time = request.POST.get("accident_time")
        accident_image = request.FILES.get("accident_image")
        user = Driver_registration.objects.get(license_id=lic)
        report = Reporting.objects.create(user=user,accident_type=accident_type,accident_desc=accident_description,accident_loc=accident_location,accident_date=accident_date,
                                 accident_time=accident_time,accident_image=accident_image)
        report.save()
        messages.success(request,"Thank you for submitting your accident report. We will review the information provided and take appropriate action.")
    return render(request, 'report.html',{'lic':lic})

def user_logout(request):
    logout(request)
    return redirect(home)
