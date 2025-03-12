from django.shortcuts import render,redirect
from User.models import *
from Guest.models import *
from Admin.models import *
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Sum
import math

def HomePage(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    return render(request,"User/HomePage.html")

def Editprofile(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_user.objects.get(id=request.session['uid'])
    if request.method=='POST':
        uname=request.POST.get('txtname')
        uemail=request.POST.get('txtemail')
        ucontact=request.POST.get('txtcontactno')
        data.user_name=uname
        data.user_email=uemail
        data.user_contact=ucontact
        data.save()
        return redirect('User:Myprofile')
    else:
        return render(request,"User/Editprofile.html",{'profeddata':data})

def Myprofile(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_user.objects.get(id=request.session['uid'])
    return render(request,"User/Myprofile.html",{'user':data})

def Changepassword(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_user.objects.get(id=request.session['uid'])
    dbpass=data.user_password
    if request.method=='POST':
        oldpass=request.POST.get('txtoldpassword')
        newpass=request.POST.get('txtnewpassword')
        confirmpass=request.POST.get('txtconfirmpassword')  
        if dbpass==oldpass:
            if newpass==confirmpass:
                data.user_password=newpass
                data.save()
                return render(request,"User/Changepassword.html",{'msg1':'Password updated'})
            else:
                return render(request,"User/Changepassword.html",{'msg':'Password does not match'})
        else:
            return render(request,"User/Changepassword.html",{'msg':'Incorrect current password '})
    else:
        return render(request,"User/Changepassword.html")

def Tool(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_tool.objects.filter(user=request.session['uid'])
    userid=tbl_user.objects.get(id=request.session['uid'])
    catdata=tbl_category.objects.all()
    if request.method=='POST':
        tname=request.POST.get('txttoolname')
        tdetails=request.POST.get('txtdetails')
        tppd=request.POST.get('txtprice')
        tqty=request.POST.get('txtquantity')
        categoryid=tbl_category.objects.get(id=request.POST.get('sel category'))
        tbl_tool.objects.create(tool_name=tname,tool_details=tdetails,tool_priceperday=tppd,user=userid,qty=tqty,category=categoryid)
        return redirect('User:Tool')
    else:
        return render(request,"User/Tool.html",{'tool':data,'cat':catdata})

def deletetool(request,did):
    tbl_tool.objects.get(id=did).delete()
    return redirect('User:Tool')

def edittool(request,eid):
    data=tbl_tool.objects.get(id=eid)
    if request.method=='POST':
        tname=request.POST.get('txttoolname')
        tdetails=request.POST.get('txtdetails')
        tppd=request.POST.get('txtprice')
        data.tool_name=tname
        data.tool_details=tdetails
        data.tool_priceperday=tppd
        data.save()
        return redirect('User:Tool')
    else:
        return render(request,"User/Tool.html",{'tooled':data})

def Gallery(request,tid):
    data=tbl_tool.objects.get(id=tid)
    if request.method=='POST':
        file=request.FILES.get('btnfile')
        tbl_gallery.objects.create(gallery_file=file,tool_id=data)
        return redirect('User:Gallery',tid)
    else:
        return render(request,"User/Gallery.html")

def Complaint(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    userid=tbl_user.objects.get(id=request.session['uid'])
    data=tbl_complaint.objects.all()
    if request.method=='POST':
        title=request.POST.get('txttitle')
        content=request.POST.get('txtcontent')
        tbl_complaint.objects.create(comp_title=title,comp_content=content,user=userid)
        return redirect('User:Complaint')
    else:
        return render(request,"User/Complaint.html",{'comp':data})

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def Viewtools(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    catdata=tbl_category.objects.all()
    ar = [1, 2, 3, 4, 5]
    parry = []
    bookmark = []
    distances = []

    # Check for current location from query parameters
    user_lat = request.GET.get("lat")
    user_lon = request.GET.get("lon")

    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
        except ValueError:
            return render(request, "User/Viewtools.html", {"error": "Invalid location parameters."})
    else:
        try:
            current_user = tbl_user.objects.get(id=request.session["uid"])
            user_lat = float(current_user.user_latitude)
            user_lon = float(current_user.user_longitude)
        except (tbl_user.DoesNotExist, ValueError):
            return render(request, "User/Viewtools.html", {"error": "Unable to determine your location."})

    data = tbl_tool.objects.filter().exclude(user__id=request.session["uid"]).select_related("user")

    tools_with_distance = []
    for tool in data:
        try:
            tool_lat = float(tool.user.user_latitude)
            tool_lon = float(tool.user.user_longitude)
            distance = haversine(user_lat, user_lon, tool_lat, tool_lon)
            distance = round(distance, 2)  # Normal distance
        except ValueError:
            distance = None  # Use None for invalid coordinates instead of float("inf")

        ratecount = tbl_rating.objects.filter(tool=tool.id).count()
        if ratecount > 0:
            avg_rating = tbl_rating.objects.filter(tool=tool.id).aggregate(Avg("rating_data"))["rating_data__avg"]
            parry.append(round(avg_rating))
        else:
            parry.append(0)

        bmark = tbl_bookmark.objects.filter(user__id=request.session["uid"], tool=tool.id).first()
        bookmark.append(bmark.id if bmark else 0)

        distances.append(distance)  # None for invalid, otherwise rounded distance
        tools_with_distance.append((tool, distance if distance is not None else float("inf")))  # Use inf for sorting

    # Sort tools by distance (None values will go to the end via float("inf"))

    print(tools_with_distance)
    tools_with_distance.sort(key=lambda x: x[1])

    sorted_tools = []
    sorted_parry = []
    sorted_bookmark = []
    sorted_distances = []

    for tool, dist in tools_with_distance:
        tool_index = [t.id for t in data].index(tool.id)  # Match tool by ID
        sorted_tools.append(tool)
        sorted_parry.append(parry[tool_index])
        sorted_bookmark.append(bookmark[tool_index])
        sorted_distances.append(dist)


    datas = zip(sorted_tools, sorted_parry, sorted_bookmark, sorted_distances)


    return render(request, "User/Viewtools.html", {
        "tool": datas,
        "ar": ar,
        "cat": catdata,
        "user_location": {"latitude": user_lat, "longitude": user_lon}
    })

# def Rentdetails(request,tid):
#     data=tbl_tool.objects.get(id=tid)
#     userid=tbl_user.objects.get(id=request.session['uid'])
#     amount = data.tool_priceperday
#     if request.method=='POST':
#         fromdate_str = request.POST.get('from_date')
#         todate_str = request.POST.get('to_date')
#         fromdate = datetime.strptime(fromdate_str, '%Y-%m-%d')
#         todate = datetime.strptime(todate_str, '%Y-%m-%d')
#         diff = todate - fromdate
#         total = int(amount) * int(diff.days)
#         tbl_renttool.objects.create(rent_tool_fromdate=fromdate,rent_tool_todate=todate,user=userid,tool=data,rent_tool_price=total)
#         return redirect('User:Rentdetails',tid)
#     else:
#         return render(request,"User/Rentdetails.html",{"amount":amount})

# def Rentdetails(request, tid):
#     data = tbl_tool.objects.get(id=tid)
#     userid = tbl_user.objects.get(id=request.session['uid'])
#     amount = data.tool_priceperday
    
#     total_qty = data.qty
#     bookings = tbl_renttool.objects.filter(
#         tool=data,
#         rent_tool_status__in=[0, 1]
#     ).values('rent_tool_fromdate', 'rent_tool_todate', 'rent_tool_qty')
    
#     booked_ranges = [
#         {
#             'from': booking['rent_tool_fromdate'].isoformat(),
#             'to': booking['rent_tool_todate'].isoformat(),
#             'qty': booking['rent_tool_qty']
#         } for booking in bookings
#     ]
    
    
#     if request.method == 'POST':
#         fromdate_str = request.POST.get('from_date')
#         todate_str = request.POST.get('to_date')
#         qty_requested = int(request.POST.get('txtquantity', 1))
        
#         fromdate = datetime.strptime(fromdate_str, '%Y-%m-%d')
#         todate = datetime.strptime(todate_str, '%Y-%m-%d')
        
#         overlapping_bookings = tbl_renttool.objects.filter(
#             tool=data,
#             rent_tool_status__in=[0, 1],
#             rent_tool_fromdate__lte=todate,
#             rent_tool_todate__gte=fromdate
#         ).aggregate(total_booked=Sum('rent_tool_qty'))['total_booked'] or 0
        
#         available_qty = total_qty - overlapping_bookings
        
#         if available_qty >= qty_requested:
#             diff = todate - fromdate
#             days=diff.days if diff.days>0 else 1
#             total = int(amount) * int(days) * qty_requested
#             tbl_renttool.objects.create(
#                 rent_tool_fromdate=fromdate,
#                 rent_tool_todate=todate,
#                 user=userid,
#                 tool=data,
#                 rent_tool_price=total,
#                 rent_tool_qty=qty_requested
#             )
#             return redirect('User:Rentdetails', tid)
#         else:
#             return render(request, "User/Rentdetails.html", {
#                 "amount": amount,
#                 "booked_ranges": booked_ranges,
#                 "tool_id": tid,
#                 "total_qty": total_qty,
#                 "error": f"Only {available_qty} units available for the selected dates"
#             })
    
#     return render(request, "User/Rentdetails.html", {
#         "amount": amount,
#         "booked_ranges": booked_ranges,
#         "tool_id": tid,
#         "total_qty": total_qty
#     })



def Rentdetails(request, tid):
    # Get tool and user data
    data = tbl_tool.objects.get(id=tid)
    userid = tbl_user.objects.get(id=request.session['uid'])
    amount = float(data.tool_priceperday)  # Convert price to float for calculation
    
    total_qty = data.qty  # Total available quantity of the tool
    # Fetch existing bookings for the tool
    bookings = tbl_renttool.objects.filter(
        tool=data,
        rent_tool_status__in=[0, 1]  # 0: pending, 1: active (adjust statuses as needed)
    ).values('rent_tool_fromdate', 'rent_tool_todate', 'rent_tool_qty')
    
    booked_ranges = [
        {
            'from': booking['rent_tool_fromdate'].isoformat(),
            'to': booking['rent_tool_todate'].isoformat(),
            'qty': booking['rent_tool_qty']
        } for booking in bookings
    ]
    
    if request.method == 'POST':
        try:
            fromdate_str = request.POST.get('from_date')
            todate_str = request.POST.get('to_date')
            qty_requested = int(request.POST.get('txtquantity', 1))
            
            # Validate quantity
            if qty_requested <= 0:
                raise ValueError("Quantity must be greater than 0")
            if qty_requested > total_qty:
                raise ValueError(f"Requested quantity ({qty_requested}) exceeds total available ({total_qty})")
            
            # Convert dates
            fromdate = datetime.strptime(fromdate_str, '%Y-%m-%d')
            todate = datetime.strptime(todate_str, '%Y-%m-%d')
            
            # Validate date range
            if todate < fromdate:
                raise ValueError("End date must be after start date")
            
            # Calculate overlapping bookings for the requested date range
            overlapping_bookings = tbl_renttool.objects.filter(
                tool=data,
                rent_tool_status__in=[0, 1],
                rent_tool_fromdate__lte=todate,  # Starts before requested end date
                rent_tool_todate__gte=fromdate   # Ends after requested start date
            ).aggregate(total_booked=Sum('rent_tool_qty'))['total_booked'] or 0
            
            # Calculate available quantity
            available_qty = total_qty - overlapping_bookings
            
            if available_qty >= qty_requested:
                # Calculate total price
                diff = (todate - fromdate).days + 1  # Include both start and end dates
                days = max(diff, 1)  # Minimum 1 day
                total = amount * days * qty_requested
                
                # Create rental record
                rentT = tbl_renttool.objects.create(
                    rent_tool_fromdate=fromdate,
                    rent_tool_todate=todate,
                    user=userid,
                    tool=data,
                    rent_tool_price=str(total),  # Convert to string as per model
                    rent_tool_qty=qty_requested
                )
                return redirect('User:Payment',rentT.id)
            else:
                return render(request, "User/Rentdetails.html", {
                    "amount": amount,
                    "booked_ranges": booked_ranges,
                    "tool_id": tid,
                    "total_qty": total_qty,
                    "available_qty": available_qty,  # Pass available qty to template
                    "error": f"Only {available_qty} units available for the selected dates"
                })
                
        except ValueError as e:
            return render(request, "User/Rentdetails.html", {
                "amount": amount,
                "booked_ranges": booked_ranges,
                "tool_id": tid,
                "total_qty": total_qty,
                "error": str(e)
            })
    
    # For GET request, calculate current availability
    overlapping_bookings = tbl_renttool.objects.filter(
        tool=data,
        rent_tool_status__in=[0, 1]
    ).aggregate(total_booked=Sum('rent_tool_qty'))['total_booked'] or 0
    available_qty = total_qty - overlapping_bookings
    
    return render(request, "User/Rentdetails.html", {
        "amount": amount,
        "booked_ranges": booked_ranges,
        "tool_id": tid,
        "total_qty": total_qty,
        "available_qty": available_qty  # Show current availability
    })

# def reqrent(request,tid):

def bookmark(request,tid,key):
    data=tbl_tool.objects.get(id=tid)
    tbl_bookmark.objects.create(tool=data,user=tbl_user.objects.get(id=request.session['uid']))
    if key=='tool':
        return redirect('User:Viewtools')
    else:
        return redirect('User:Viewbookmarks')

def Viewbookmarks(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_bookmark.objects.filter(user=request.session['uid'])
    return render(request,"User/Viewbookmarks.html",{"bmark":data})

def deletebookmark(request,did,key):
    tbl_bookmark.objects.get(id=did).delete()
    if key=='tool':
        return redirect('User:Viewtools')
    else:
        return redirect('User:Viewbookmarks')

def Mybooking(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_renttool.objects.filter(user=request.session['uid'])
    return render(request,"User/Mybooking.html",{"book":data})

def Viewbooking(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_renttool.objects.filter(tool__user=request.session['uid'])
    return render(request,"User/Viewbooking.html",{"book":data})

def returned(request,ret_id):
    data=tbl_renttool.objects.get(id=ret_id)
    data.rent_tool_status=2
    data.save()
    return redirect('User:Viewbooking') 

def acceptbooking(request,acc_id):
    data=tbl_renttool.objects.get(id=acc_id)
    data.rent_tool_status=1
    data.save()
    return redirect('User:Viewbooking')
        

def rejectbooking(request,rej_id):
    data=tbl_renttool.objects.get(id=rej_id)
    data.rent_tool_status=2
    data.save()
    return redirect('User:Viewbooking')

def rating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
    counts=0
    counts=stardata=tbl_rating.objects.filter(tool=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(tool=mid).order_by('-rating_datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        return render(request,"User/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"User/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    user_id=tbl_user.objects.get(id=request.session['uid'])
    rating_review=request.GET.get('rating_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=user_id,rating_review=rating_review,rating_data=rating_data,tool=tbl_tool.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(tool=pid).order_by('-rating_datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(tool=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(tool=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)


def chatpage(request,id):
    user  = tbl_user.objects.get(id=id)
    return render(request,"User/Chat.html",{"user":user})

def ajaxchat(request):
    from_user = tbl_user.objects.get(id=request.session["uid"])
    to_user = tbl_user.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),user_from=from_user,user_to=to_user,chat_file=request.FILES.get("file"))
    return render(request,"User/Chat.html")

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_user.objects.get(id=request.session["uid"])
    chat_data = tbl_chat.objects.filter((Q(user_from=user) | Q(user_to=user)) & (Q(user_from=tid) | Q(user_to=tid))).order_by('chat_time')
    return render(request,"User/ChatView.html",{"data":chat_data,"tid":int(tid)})

def clearchat(request):
    tbl_chat.objects.filter(Q(user_from=request.session["uid"]) & Q(user_to=request.GET.get("tid")) | (Q(user_from=request.GET.get("tid")) & Q(user_to=request.session["uid"]))).delete()
    return render(request,"User/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})

def ajaxsearchtool(request):
    ar = [1, 2, 3, 4, 5]
    parry = []
    bookmark = []
    distances = []

    # Check for current location from query parameters
    user_lat = request.GET.get("lat")
    user_lon = request.GET.get("lon")

    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
        except ValueError:
            return render(request, "User/Viewtools.html", {"error": "Invalid location parameters."})
    else:
        try:
            current_user = tbl_user.objects.get(id=request.session["uid"])
            user_lat = float(current_user.user_latitude)
            user_lon = float(current_user.user_longitude)
        except (tbl_user.DoesNotExist, ValueError):
            return render(request, "User/Viewtools.html", {"error": "Unable to determine your location."})

    data = tbl_tool.objects.filter(category=request.GET.get("catid")).exclude(user__id=request.session["uid"]).select_related("user")

    tools_with_distance = []
    for tool in data:
        try:
            tool_lat = float(tool.user.user_latitude)
            tool_lon = float(tool.user.user_longitude)
            distance = haversine(user_lat, user_lon, tool_lat, tool_lon)
            distance = round(distance, 2)  # Normal distance
        except ValueError:
            distance = None  # Use None for invalid coordinates instead of float("inf")

        ratecount = tbl_rating.objects.filter(tool=tool.id).count()
        if ratecount > 0:
            avg_rating = tbl_rating.objects.filter(tool=tool.id).aggregate(Avg("rating_data"))["rating_data__avg"]
            parry.append(round(avg_rating))
        else:
            parry.append(0)

        bmark = tbl_bookmark.objects.filter(user__id=request.session["uid"], tool=tool.id).first()
        bookmark.append(bmark.id if bmark else 0)

        distances.append(distance)  # None for invalid, otherwise rounded distance
        tools_with_distance.append((tool, distance if distance is not None else float("inf")))  # Use inf for sorting

    # Sort tools by distance (None values will go to the end via float("inf"))
    tools_with_distance.sort(key=lambda x: x[1])
    sorted_tools = [t[0] for t in tools_with_distance]

    datas = zip(sorted_tools, parry, bookmark, distances)

    return render(request, "User/AjaxSearchTool.html", {
        "tool": datas,
        "ar": ar,
        "user_location": {"latitude": user_lat, "longitude": user_lon}
    })

def Payment(request,id):
   booking = tbl_renttool.objects.get(id=id)
#    scrap = tbl_Scrap.objects.get(id=booking.scarp.id)
   amount = booking.rent_tool_price
   if request.method == "POST":
      booking.rent_tool_status = 1
      booking.save()
      return redirect("User:Loader")
   else:
      return render(request,"User/Payment.html", {"total":amount})

def Loader(request):
    return render(request,"User/Loader.html")

def Payment_suc(request):
    return render(request,"User/Payment_suc.html")