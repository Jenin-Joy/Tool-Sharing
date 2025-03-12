from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *

def Login(request):
    if request.method == "POST":
        email=request.POST.get("txtemail")
        password=request.POST.get("txtpassword")
        admincount=tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        usercount=tbl_user.objects.filter(user_email=email,user_password=password).count()

        if usercount>0:
            user=tbl_user.objects.get(user_email=email,user_password=password)
            if user.user_status==1:
                return render(request,"Guest/Login.html",{'msg':"Your Account is not Active"})
            else:
                request.session['uid']=user.id
                return redirect('User:HomePage')
        elif admincount>0:
            admin=tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session['admid']=admin.id
            return redirect('Admin:HomePage')
        else:
            return render(request,"Guest/Login.html",{'msg':"Invalid Email or Password"})
    else:
        return render(request,"Guest/Login.html")

def Logout(request):
    if 'uid' in request.session:
        del request.session["uid"]
    if 'admid' in request.session:
        del request.session["admid"]
    return redirect("Guest:Login")

def UserRegistration(request):
    data=tbl_user.objects.all()
    if request.method =="POST":
        uname=request.POST.get("txtname")
        uemail=request.POST.get("txtemail")
        ucontact=request.POST.get("txtcontactno") 
        lat=request.POST.get("latitude")
        long=request.POST.get("longitude")
        uphoto=request.FILES.get("fphoto")
        uproof=request.FILES.get("fproof")
        upass=request.POST.get("txtpassword")
        tbl_user.objects.create(user_name=uname,user_email=uemail,user_contact=ucontact,user_latitude=lat,user_longitude=long,user_photo=uphoto,user_proof=uproof,user_password=upass) 
        return redirect('Guest:Login')
    else:
        return render(request,"Guest/UserRegistration.html",{"udata":data})