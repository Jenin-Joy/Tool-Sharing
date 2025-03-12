from django.db import models

class tbl_user(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.EmailField(max_length=50)
    user_password=models.CharField(max_length=50)
    user_proof=models.FileField(upload_to="Assets/User/")   
    user_photo=models.FileField(upload_to="Assets/User/")
    user_contact=models.CharField(max_length=50)
    user_latitude=models.CharField(max_length=50)
    user_longitude=models.CharField(max_length=50)
    user_status=models.IntegerField(default=0)  
