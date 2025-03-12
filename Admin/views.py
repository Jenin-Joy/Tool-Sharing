from django.shortcuts import render,redirect
from Admin.models import *
from User.models import *

def HomePage(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    return render(request,"Admin/HomePage.html")

def Category(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    catdata=tbl_category.objects.all()
    if request.method == "POST":
        catname = request.POST.get("cname")
        tbl_category.objects.create(category_name=catname)
        return redirect('Admin:Category')
    else:
        return render(request,"Admin/Category.html",{"cat":catdata})

def deletecat(request,did):
    tbl_category.objects.get(id=did).delete()
    return redirect('Admin:Category')

def editcat(request,eid):
    data=tbl_category.objects.get(id=eid)
    if request.method=='POST':
        categoryname=request.POST.get("cname")
        data.category_name=categoryname
        data.save()
        return redirect('Admin:Category')       
    else:
        return render(request,"Admin/Category.html",{"cated":data})


def AdminRegistration(request):
    admindata=tbl_admin.objects.all()
    if request.method == "POST":
        adminname = request.POST.get("admname")
        adminemail = request.POST.get("admemail")
        adminpassword = request.POST.get("admpassword")
        tbl_admin.objects.create(admin_name=adminname,admin_email=adminemail,admin_password=adminpassword)
        return redirect('Admin:AdminRegistration')
    else:
        return render(request,"Admin/AdminRegistration.html",{"adm":admindata})
        
def deleteadmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return redirect('Admin:AdminRegistration')

def editadmin(request,eid):
    data=tbl_admin.objects.get(id=eid)
    if request.method=='POST':
        adminname=request.POST.get("admname")
        adminemail=request.POST.get("admemail")
        adminpassword=request.POST.get("admpassword")
        data.admin_name=adminname
        data.admin_email=adminemail
        data.admin_password=adminpassword
        data.save()
        return redirect('Admin:AdminRegistration')       
    else:
        return render(request,"Admin/AdminRegistration.html",{"admed":data})


def Viewcomplaint(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_complaint.objects.all()
    if request.method=='POST':
        return redirect('Admin:Reply')
    else:
        return render(request,"Admin/Viewcomplaint.html",{"comp":data})

def Reply(request,rid):
    data=tbl_complaint.objects.get(id=rid)  
    if request.method=='POST':
        reply=request.POST.get("reply")
        data.comp_reply=reply
        data.comp_status=1
        data.save()
        return redirect('Admin:Repliedcomplaints')
    else:
        return render(request,"Admin/Reply.html") 

def Repliedcomplaints(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_complaint.objects.all()
    return render(request,"Admin/Repliedcomplaints.html",{"repcomp":data})  

def Viewallusers(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_user.objects.all()
    return render(request,"Admin/Viewallusers.html",{"user":data})  

def Viewusertooldetails(request,uid):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    utooldata=tbl_tool.objects.filter(user=uid)
    urentdata=tbl_renttool.objects.filter(user=uid)
    urentaldata=tbl_renttool.objects.filter(tool__user=uid)
    return render(request,"Admin/Viewusertooldetails.html",{"utool":utooldata,"urent":urentdata,"urental":urentaldata})

def blockuser(request,id, status):
    data=tbl_user.objects.get(id=id)
    data.user_status=status
    data.save()
    return redirect('Admin:Viewallusers')
