from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random, time
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from datetime import datetime,timedelta
from .models import *
from user.models import *
from django.core.mail import send_mail
from django.conf import settings
from tpo.models import *

# Create your views here.
def dashboard(request):
    paid_fee = 0
    unpaid_fee = 0
    lic = request.session.get('id')
    fines = IssueFine.objects.all()
    for f in fines:
        if f.status == 'pending':
            unpaid_fee += f.total_amount
        else:
            paid_fee += f.total_amount
    traffic_officer_count=Traffic_police.objects.all().count()
    provision_count=Fine_tickets.objects.all().count()
    total_drivers_count=Driver_registration.objects.all().count()

    context={"provision_count":provision_count,
             'traffic_officer_count':traffic_officer_count,
             'total_drivers_count':total_drivers_count,
             'pending':unpaid_fee,
             'paid':paid_fee}
    return render(request,'dashboard.html',context=context)


def register(request):
    if request.method == 'POST':
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        Username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        print(fullname, email, password, password1)
        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email Already Exist!')
            elif User.objects.filter(username=Username).exists():
                messages.warning(request, 'Username Already Exists!')

            else:
                user = User.objects.create_user(first_name=fullname, username=email, email=email, password=password)
                user.save()
                return redirect(signin)
                print('user saved')
        else:
            messages.warning(request, 'Password Missmatch')

    return render(request, 'register.html')


def signin(request):
    if request.method=='POST':
        email= request.POST.get('admin_email')
        password= request.POST.get('admin_password')
        print(email,password)
        user=authenticate(request, username=email,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect(dashboard)
        else:
            messages.warning(request, 'invalid login')
    return render(request, "index1.html")


def forgot(request):
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
        newpass=request.POST.get('password')
        confirmpass=request.POST.get('confirmpassword')
        print(newpass,confirmpass)
        if otp==confirm_otp and  newpass==confirmpass and diff <= timedelta(minutes=5):
            user=User.objects.get(username=user)
            user.set_password(newpass)
            user.save()
            user_login=authenticate(request,username=user.username,password=newpass)
            if user_login is not None:
                login(request,user_login)
                return redirect(dashboard)
            else:
                messages.error(request,'account not found')
        elif otp!=confirm_otp:
            messages.error(request,'invalid otp')
        elif newpass!=confirmpass:
            messages.error(request,'password missmatch')
        elif otp==confirm_otp and diff >= timedelta(minutes=5):
            messages.error(request, "Time exceeded!")

    return render(request, 'forgotpassword.html')


def otp(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            if User.objects.get(username=email):
                def generate_otp():
                    return random.randint(1000, 9999)

                otp = generate_otp()
                time=datetime.now()
                print('generated_otp', otp)
                # time.sleep(300)
                send_mail('forgot password', f'otp for your password reset:{otp}', settings.EMAIL_HOST_USER, [email])
                request.session['otp']=otp
                request.session['username']=email
                request.session['time']=str(time)
                return redirect('forgotpass')
        except:
            messages.warning(request, "Email doesn't exist")
            # return render(request, 'otpverification.html',{'messages':"Email doesn't exist"})

    return render(request, 'otpverification.html')

def guest(request):
    return render(request ,"index.html")
def admin(request):
    return render(request ,"index1.html")

def signout(request):
    logout(request)
    return redirect(signin)

def tpo(request):
    return render(request ,"home.html")

def add_traffic_officer(request):
    if request.method == 'POST':
        id = request.POST.get('officerid')
        email = request.POST.get('officeremail')
        password = request.POST.get('officerpassword')
        confirm_password = request.POST.get('officerpasswordconfirm')
        name = request.POST.get('officername')
        police_station = request.POST.get('policestation')
        court = request.POST.get('tpocourt')
        registered_date = request.POST.get('registereddate')
        if password==confirm_password:
            if Traffic_police.objects.filter(officer_email=email).exists():
                messages.error(request,'email exists')
            elif Traffic_police.objects.filter(police_id=id).exists():
                messages.error(request,'id exists')
            else:
                add_traffic_police=Traffic_police.objects.create(police_id=id,officer_email=email,officer_password=password,
                                                                 officer_name=name,police_station=police_station,court=court,
                                                                 registered_at=registered_date)
                add_traffic_police.save()
                send_mail("Registration Successful", f"Your request for traffic portal has been successfull!... Your Police ID is {id} and Password is {password}", settings.EMAIL_HOST_USER,[email])
                messages.success(request,"Traffic police added successfully!!")
                print('police_added')
        else:
            messages.error(request,'password mismatch')
    return render(request ,"add_traffic_officer.html")

def view_all_traffic_officers(request):
    all_traffic_officers=Traffic_police.objects.all()
    return render(request ,"view_all_traffic_officers.html",{'all_traffic_officers':all_traffic_officers})

def delete_officers(request):
    id=request.GET.get('id')
    officer = Traffic_police.objects.get(id=id)
    officer.delete()
    print("officer deleted!")
    return redirect(view_all_traffic_officers)

def edit_officers(request):
    id=request.GET.get('id')
    officer =Traffic_police.objects.get(id=id)
    if request.method == 'POST':
        email = request.POST.get('officeremail')
        name = request.POST.get('officername')
        police_station = request.POST.get('policestation')
        court = request.POST.get('tpocourt')
        registered_date = request.POST.get('registereddate')
        officer.officer_email=email
        officer.officer_name=name
        officer.police_station=police_station
        officer.court=court
        officer.registered_at=registered_date
        officer.save()
        return redirect(view_all_traffic_officers)
        print("police upadated")
    return render(request,'edit_traffic_officer.html',{'id':officer})

def mtd_account(request):
    if request.method=='POST':
        if request.POST.get('formtype')=='form1':
            email=request.POST.get('changeemail')
            if User.objects.filter(username=email).exists():
                messages.error(request,'The current email is already exists... try another one!!')
            else:
                user=User.objects.get(id=request.user.id)
                user.username=email
                user.email=email
                user.save()
                print("email changed")
                messages.success(request,'Email changed successfully!!')
        elif request.POST.get('formtype')=='form2':
            password=request.POST.get('newpassword')
            cpassword=request.POST.get('passwordconfirm')
            if password==cpassword:
                user=User.objects.get(id=request.user.id)
                user.set_password(password)
                user.save()
                print('password changed')
                messages.success(request, 'Password changed successfully!!')
            else:
                messages.error(request,'password mismatch')
    return render(request ,"mtd_account.html")

def fine_tickets(request):
    all_fine_tickets = Fine_tickets.objects.all()
    if request.method=='POST':
        section_of_act=request.POST.get('sectionofact')
        provision=request.POST.get('provision')
        fine_amount=request.POST.get('fineamount')
        print(section_of_act,provision,fine_amount)
        fine=Fine_tickets.objects.create(section_of_act=section_of_act,
                                          provision=provision,
                                          fine_amount=fine_amount)
        fine.save()
        print('fine_added')
        messages.success(request,'Fine added!!')
    return render(request ,"fine_tickets.html",{'all_fines':all_fine_tickets})


def edit_fine_tickets(request):
    id=request.GET.get('id')
    print(id)
    all_fine_tickets = Fine_tickets.objects.all()
    fines=Fine_tickets.objects.get(id=id)
    if request.method=='POST':
        section_of_act=request.POST.get('sectionofact')
        provision=request.POST.get('provision')
        fine_amount=request.POST.get('fineamount')
        print(section_of_act,provision,fine_amount)
        fines.section_of_act=section_of_act
        fines.provision=provision
        fines.fine_amount=fine_amount
        fines.save()
        return redirect(fine_tickets)

    return render(request ,"fine_tickets.html",{'all_fines':all_fine_tickets,'fines':fines})


def delete_fines(request):
    id=request.GET.get('id')
    fine = Fine_tickets.objects.get(id=id)
    fine.delete()
    print("fine deleted!")
    return redirect(fine_tickets)


def view_drivers(request):
    all_drivers=Driver_registration.objects.all()
    return render(request ,"view_all_drivers.html",{'all_drivers':all_drivers})

def delete_drivers(request):
    id=request.GET.get('id')
    driver = Driver_registration.objects.get(id=id)
    driver.delete()
    print("driver deleted!")
    return redirect(view_drivers)

def paid_fine_tickets(request):
    paid = IssueFine.objects.filter(status="paid")
    return render(request ,"paid_fine_tickets.html",{'paid':paid})

def pending_fine_tickets(request):
    pending = IssueFine.objects.filter(status="pending")
    return render(request ,"pending_fine_tickets.html",{'pending':pending})

def reported_issues(request):
    report = Reporting.objects.all()
    return render(request,"reported_issues.html", {'report':report})

def admin_signout(request):
    logout(request)
    return redirect(guest)