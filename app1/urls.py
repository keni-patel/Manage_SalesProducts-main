from django.urls import path

# from . import views as v
from .views import *

urlpatterns = [
    # -------------------- company -------------
    path('',Company_login,name='c_login'),
    path('Registration/',Company_regi,name='c_regi'),
    path('CompForgetPass/',CompForgetPass,name='CompForgetPass'),
    path('OTP_check/',OTP_check,name='OTP_check'),
    path('New_Password/',New_Password,name='New_Password'),
    path('DashBoard/',ComDashBoard,name='ComDashBoard'),
    path('Profile_Manage/',Profile_Manage,name='Profile_Manage'),
    path('AddCompCustomer/',AddCompCustomer,name='AddCompCustomer'),
    path('ViewCustomer/',ViewCustomer,name='ViewCustomer'),
    path('DeleteCustomer/<int:id>',DeleteCustomer,name='DeleteCustomer'),
    path('vieworder/',Vieworder,name='vieworder'),
    path('yesorder/<int:id>',YESorder,name='yesorder'),
    path('noorder/<int:id>',NOorder,name='noorder'),
    path('Logout_Comp/',Logout_Comp,name='Logout_Comp'),
    
    # -------------------- Product ----------------
    path('AddProduct/',AddProduct,name='AddProduct'),
    path('ViewProduct/',ViewProduct,name='ViewProduct'),
    path('DeleteProduct/<int:id>',DeleteProduct,name='DeleteProduct'),
    path('UpdateProduct/<int:id>',UpdateProduct,name='UpdateProduct'),
    
    # -------------------- customer -------------
    path('Customer_Login/',Customer_Login,name='Customer_Login'),
    path('Customer_dash/',Customer_dash,name='Customer_dash'),
    path('Profile/',Profile,name='Profile'),
    path('order_place/<int:id>',order_place,name='order_place'),
    path('order/',Customer_order,name='order'),
    path('Customer_logout/',Customer_logout,name='Customer_logout'),
]
