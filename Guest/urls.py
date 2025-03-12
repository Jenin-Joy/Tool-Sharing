from django.urls import path,include
from Guest import views
app_name = 'Guest'

urlpatterns = [
    path('Login/',views.Login, name="Login"),  
    path('Logout/',views.Logout,name="Logout"),
    path('UserRegistration/',views.UserRegistration, name="UserRegistration"),
]