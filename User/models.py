from django.db import models
from Admin.models import *
from Guest.models import *

class tbl_tool(models.Model):
  tool_name=models.CharField(max_length=50)
  tool_details=models.CharField(max_length=50)
  tool_priceperday=models.CharField(max_length=50)
  user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
  tool_status=models.IntegerField(default=0)
  qty=models.IntegerField(default=1)
  category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
  

class tbl_gallery(models.Model):
  gallery_file=models.FileField(upload_to='Assets/gallery/')
  tool=models.ForeignKey(tbl_tool,on_delete=models.CASCADE)
   
class tbl_complaint(models.Model):
  comp_title=models.CharField(max_length=50)
  comp_content=models.CharField(max_length=50)
  user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
  comp_reply=models.CharField(max_length=50)
  comp_date=models.DateField(auto_now_add=True)
  comp_status=models.IntegerField(default=0)

class tbl_renttool(models.Model):
  rent_tool_date=models.DateField(auto_now_add=True)
  rent_tool_fromdate=models.DateField()
  rent_tool_todate=models.DateField()
  user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
  tool=models.ForeignKey(tbl_tool,on_delete=models.CASCADE)
  rent_tool_status=models.IntegerField(default=0)
  rent_tool_price=models.CharField(max_length=50)
  rent_tool_qty=models.IntegerField(default=1)


class tbl_bookmark(models.Model):
  bookmark_date=models.DateField(auto_now_add=True)
  tool=models.ForeignKey(tbl_tool,on_delete=models.CASCADE)
  user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
  
class tbl_rating(models.Model):
  rating_review=models.CharField(max_length=50)
  user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
  tool=models.ForeignKey(tbl_tool,on_delete=models.CASCADE)
  rating_data=models.IntegerField()
  rating_datetime=models.DateTimeField(auto_now_add=True)


class tbl_chat(models.Model):
  chat_content = models.CharField(max_length=500)
  chat_time = models.DateTimeField()
  chat_file = models.FileField(upload_to='ChatFiles/')
  user_from = models.ForeignKey(tbl_user,on_delete=models.CASCADE,related_name="user_from")
  user_to = models.ForeignKey(tbl_user,on_delete=models.CASCADE,related_name="user_to")