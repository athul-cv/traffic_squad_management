from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from police.models import Traffic_police, Fine_tickets
from user.models import Driver_registration
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import random
from datetime import datetime, timedelta
from mtd.models import *
from user.models import *
# Create your views here.

def police_login(request):
    if request.method == 'POST':
        police_id = request.POST.get('police_id')
        officer_password = request.POST.get('officer_password')
        if Traffic_police.objects.filter(police_id=police_id, officer_password=officer_password).exists():
            request.session['id'] = police_id
            return redirect(police_dashboard,police_id)
        else:
            messages.error(request,"Invalid Login")
        
    return render(request,'police_login.html')

def police_home(request):
    return render(request,'police_home.html')

def forgot_password(request):
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
                return redirect(tpo_reset_password)
        except:
            messages.warning(request, "Email doesn't exist")
    return render(request,'forgot-password.html')



def tpo_reset_password(request):
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
            user=Traffic_police.objects.get(officer_email=user)
            user.officer_password=newpass
            user.save()
            return redirect(police_login)
        elif otp!=confirm_otp:
            messages.error(request,'Invalid OTP')
        elif newpass!=confirmpass:
            messages.error(request,'Password Mismatch')
        elif otp==confirm_otp and diff >= timedelta(minutes=5):
            messages.error(request, "Time Exceeded!")

    return render(request, 'tpo_reset_password.html')

def police_dashboard(request,pid):
    print(request.session.get('id'))
    request.session['id'] = request.session.get('id')
    return render(request,'police_dashboard.html',{'pid':request.session.get('id'),'pid':pid})

def add_new_fine(request, pid):
    print(pid)
    if request.method == "POST":
        if request.POST.get('formtype') == "search":
            license_id = request.POST.get('licenseid')
            print(license_id)
            try:
                l_id = Driver_registration.objects.get(license_id=license_id)
                p_id = Traffic_police.objects.get(police_id=pid)
                fine  =  Fine_tickets.objects.all()
                print(fine)
                return render(request, 'add_new_fine.html',{'lid':l_id,'pid':pid, 'p_id':p_id,'fine':fine})
            except:
                messages.error(request,"License ID not found!")

        elif request.POST.get('formtype') == "fine":
            license = request.POST.get('license')
            drivername = request.POST.get('drivername')
            homeaddress = request.POST.get('homeaddress')
            classofvehicle = request.POST.get('classofvehicle')
            policeid = request.POST.get('policeid')
            officername = request.POST.get('officername')
            policestation = request.POST.get('policestation')
            court = request.POST.get('court')
            issuedated = request.POST.get('issuedated')
            issuetimed = request.POST.get('issuetimed')
            expiredated = request.POST.get('expiredated')
            courtdated = request.POST.get('courtdated')
            place = request.POST.get('place')
            vehicleno = request.POST.get('vehicleno')
            province = request.POST.get('province')
            fined = request.POST.get('fined')
            print(license,classofvehicle,policeid,issuedated,issuetimed,expiredated,courtdated,place,vehicleno,province,fined)
            issued_fine = IssueFine.objects.create(ref_no = random.randint(10000,100000),police_id=policeid,
                                                   license_id=license,vehicle_no=vehicleno,class_of_vehicle=classofvehicle,
                                                   place=place,issued_date=issuedated,issued_time=issuetimed,expired_date=expiredated,
                                                   court_date=courtdated,provision=province,total_amount=fined,status="pending"
                                                )
            issued_fine.save()
            print("fined")
            messages.success(request,"Fine issued!")
    return render(request,'add_new_fine.html',{'pid':pid})

def check_revenue_license(request,pid):
    print(pid)
    if request.method == "POST":
        vehicle = request.POST.get('vehicle')
        try:
            veh = Add_vehicle.objects.get(vehicle_no=vehicle)
            return render(request, 'check_revenue_license.html', {'pid': pid,'v':veh})
        except:
            messages.error(request, "Vehicle No. not found!")
    return render(request,'check_revenue_license.html',{'pid':pid})

def view_reported_fine(request,pid):
    reports = IssueFine.objects.filter(police_id=pid)
    return render(request,'view_reported_fine.html',{'pid':pid,'reports':reports})

def view_reported_fine_table(request):
    return render(request,'view_reported_fine_table.html')

def police_profile(request, pid):
    p_id = Traffic_police.objects.get(police_id=pid)
    if request.method == "POST":
        old = request.POST.get('oldpassword')
        new = request.POST.get('newpassword')
        confirm = request.POST.get('passwordconfirm')
        if new == confirm:
            if old == p_id.officer_password:
                p_id.officer_password=new
                p_id.save()
                messages.success(request,"Password changed successfully!!")
            else:
                messages.error(request, "Current Password Incorrect!!")
        else:
            messages.error(request, "Password mismatch!!")
    return render(request,'police_profile.html',{'pid':pid,'p':p_id})

def profile_details(request,pid):
    p_id = Traffic_police.objects.get(police_id=pid)
    return render(request,'police_profile_details.html', {'pid':pid,'p':p_id})

def verification_code(request):
    return render(request,'verification-code.html')


def user_reported_issues(request,pid):
    report = Reporting.objects.all()
    return render(request,"user_reported_issues.html", {'report':report,'pid':pid})

def tpo_logout(request):
    logout(request)
    return redirect(police_login)