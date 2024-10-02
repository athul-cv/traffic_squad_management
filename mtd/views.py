from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from user.models import Driver_registration
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail
from django.conf import settings
import matplotlib.pyplot as plt
from .models import *
import random
from io import BytesIO
import base64

# Create your views here.

def mtd_login(request):
    if request.method == 'POST':
        email = request.POST.get('mtd_email')
        password = request.POST.get('mtd_password')
        print(email, password)
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(mtd_dashboard)
        else:
            messages.warning(request, 'invalid login')
    return render(request, 'mtd_login.html')


def mtd_forgot_password(request):
    if request.method=='POST':
        email = request.POST.get('email')
        print(email)
        try:
            if User.objects.get(username=email):
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
                return redirect(new_password)
        except:
            messages.error(request, "Email doesn't exist")
    return render(request, 'mtd_forgot-password.html')


def new_password(request):
    otp = request.session.get('otp')
    user = request.session.get('username')
    time = request.session.get('time')
    send_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    print("ttt", send_time.hour, send_time.minute, send_time.second)
    end_time = datetime.now()
    diff = end_time - send_time
    print(diff)
    print(timedelta(minutes=5))
    if request.method == 'POST':
        confirm_otp = int(request.POST.get('otp'))
        print(confirm_otp, type(confirm_otp))
        newpass = request.POST.get('password')
        confirmpass = request.POST.get('cpassword')
        print(newpass, confirmpass)
        if otp == confirm_otp and newpass == confirmpass and diff <= timedelta(minutes=5):
            user = User.objects.get(username=user)
            user.set_password(newpass)
            user.save()
            user_login = authenticate(request, username=user.username, password=newpass)
            if user_login is not None:
                login(request, user_login)
                return redirect(mtd_dashboard)
            else:
                messages.error(request, 'account not found')
        elif otp != confirm_otp:
            messages.error(request, 'invalid otp')
        elif newpass != confirmpass:
            messages.error(request, 'password missmatch')
        elif otp == confirm_otp and diff >= timedelta(minutes=5):
            messages.error(request, "Time exceeded!")
    return render(request, 'new_password.html')


def mtd_home(request):
    return render(request, 'mtd_home.html')


def mtd_dashboard(request):
    drivers = Driver_registration.objects.all().count()
    # Get current date
    current_date = datetime.now()

    # Last 7 days
    last_7_days = current_date - timedelta(days=7)
    drivers_last_7_days = Driver_registration.objects.filter(registered_at__gte=last_7_days).count()

    # Last month
    last_month = current_date - timedelta(days=30)
    drivers_last_month = Driver_registration.objects.filter(registered_at__gte=last_month).count()

    # Last year
    last_year = current_date - timedelta(days=365)
    drivers_last_year = Driver_registration.objects.filter(registered_at__gte=last_year).count()

    # Number of drivers for each category
    # all_drivers_count = Driver_registration.objects.all().count()
    # drivers_last_7_days_count = drivers_last_7_days
    # drivers_last_month_count = drivers_last_month
    # drivers_last_year_count = drivers_last_year
    #
    # # Categories
    # categories = ['All Drivers', 'Last 7 Days', 'Last Month', 'Last Year']
    # counts = [all_drivers_count, drivers_last_7_days_count, drivers_last_month_count, drivers_last_year_count]
    #
    # # Creating the bar graph
    # plt.bar(categories, counts, color=['blue', 'green', 'orange', 'red'])
    # plt.xlabel('Time Period')
    # plt.ylabel('Number of Drivers')
    # plt.title('Number of Drivers Registered')
    #
    # # Save the plot to a BytesIO object
    # buffer = BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    #
    # # Encode the plot in base64
    # plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    # buffer.close()

    return render(request, 'mtd_dashboard.html',{'d':drivers, 'last_7_days':drivers_last_7_days, 'last_month':drivers_last_month, 'last_year':drivers_last_year})


def add_driver(request):
    if request.method == 'POST':
        license_id = request.POST.get('licenseid')
        email = request.POST.get('driveremail')
        password = request.POST.get('driverpassword')
        cpassword = request.POST.get('cdriverpassword')
        name = request.POST.get('drivername')
        class_of_vechicle = request.POST.get('classofvehicle')
        address = request.POST.get('homeaddress')
        license_issue_date = request.POST.get('licenseissuedate')
        license_expire_date = request.POST.get('licenseexpiredate')
        registered_date = request.POST.get('registereddate')
        licenseissuedate = datetime.strptime(license_issue_date, "%Y-%m-%d")
        licenseexpiredate = datetime.strptime(license_expire_date, "%Y-%m-%d")
        # print(type(licenseexpiredate))
        # print(LicenseID, DriverEmail, Drivername, licenseissuedate, licenseexpiredate)
        if password == cpassword:
            if Driver_registration.objects.filter(driver_email=email).exists():
                messages.warning(request, 'email exists')
            elif Driver_registration.objects.filter(license_id=license_id).exists():
                messages.warning(request, 'id exists')
            elif licenseissuedate >= licenseexpiredate:
                messages.warning(request, 'expiration date must be after the issue date')
            elif licenseexpiredate <= datetime.now():
                messages.warning(request, "license expiration date can't be in the past")
            else:
                driver = Driver_registration.objects.create(license_id=license_id,
                                                            driver_email=email,
                                                            driver_password=password,
                                                            driver_name=name,
                                                            address=address,
                                                            class_of_vehicle=class_of_vechicle,
                                                            license_issue_date=license_issue_date,
                                                            license_expire_date=license_expire_date,
                                                            registered_at=registered_date)
                driver.save()
                send_mail("Registration Successful", f"Your request for driver registration has been successfull!... Your License ID is {license_id} and Password is {password}", settings.EMAIL_HOST_USER,[email])
                print('driver_added')
        else:
            messages.warning(request, 'password mismatch')

    return render(request, 'add_driver.html')


def view_all_driver(request):
    drivers = Driver_registration.objects.all()
    return render(request, 'view_all_driver.html', {'drivers': drivers})


def edit_driver(request):
    id = request.GET.get('id')
    driver = Driver_registration.objects.get(id=id)
    if request.method == "POST":
        email = request.POST.get('driveremail')
        name = request.POST.get('drivername')
        class_of_vechicle = request.POST.get('classofvehicle')
        address = request.POST.get('homeaddress')
        driver = Driver_registration.objects.get(id=id)
        driver.driver_email = email
        driver.driver_name = name
        driver.class_of_vehicle = class_of_vechicle
        driver.address = address
        driver.save()
        messages.success(request,"Driver Updated Successfully !!")
    return render(request, 'edit_driver.html',{'driver': driver})


def delete_drivers(request):
    id = request.GET.get('id')
    drivers = Driver_registration.objects.get(id=id)
    drivers.delete()
    print("driver deleted!")
    return redirect(view_all_driver)


def view_all_drivers_delete_modal(request):
    return render(request, 'view_all_drivers_delete_modal.html')


def mtd_profile(request):
    if request.method == "POST":
        old = request.POST.get('oldpassword')
        new = request.POST.get('newpassword')
        confirm = request.POST.get('passwordconfirm')
        if new == confirm:
            current = User.objects.get(id=request.user.id)
            user = authenticate(request, username=current.username, password=old)
            print("user",user)
            if current.check_password(old):
                current.set_password(new)
                current.save()
                print("password changed")
                messages.success(request,"Password changed successfully !!")
            else:
                messages.error(request,"Current Password Incorrect!!")
        else:
            messages.error(request,"Password mismatch!!")

    return render(request, 'mtd_profile.html')


def verification_code(request):
    return render(request, 'verification-code.html')


def add_vehicle(request):
    if request.method == 'POST':
        vehicle = request.POST.get('vehicle')
        vehicle_type = request.POST.get('vehicle_type')
        fuel_type = request.POST.get('fuel_type')
        license_id = request.POST.get('license_id')
        if not Driver_registration.objects.filter(license_id=license_id).exists():
            messages.error(request,"Incorrect License ID !!")
        else:
            lic = Driver_registration.objects.get(license_id=license_id)
            veh = Add_vehicle.objects.create(vehicle_no=vehicle,vehicle_type=vehicle_type,fuel_type=fuel_type,
                                             license_id=lic)
            veh.save()
            messages.success(request,"Vehicle added!")
    return render(request,'add_vehicle.html')

def mtd_logout(request):
    logout(request)
    return redirect(mtd_login)
