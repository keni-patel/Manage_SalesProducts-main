from django.db import models
from django.db.models.base import ModelState

# Create your models here.

class Company_data(models.Model):
    com_name = models.CharField(default="",max_length=200)
    com_em = models.EmailField(default="",max_length=200)
    com_cno = models.PositiveIntegerField(default=0)
    com_add = models.TextField(default="")
    join_date = models.DateField(auto_now=True,blank=True, null=True) 
    profile = models.ImageField(upload_to="Comp_Profile/",default="",max_length=300,blank=True, null=True)
    com_pass = models.CharField(default="",max_length=200)
    

class Company_Customer(models.Model):
    comp = models.ForeignKey('Company_data',on_delete=models.CASCADE,blank=True,null=True)
    cust_nm = models.CharField(default="",max_length=200)
    cust_em = models.EmailField(default="",max_length=200)
    cust_con = models.PositiveIntegerField(default=0)
    cust_add1 = models.TextField(default="")
    cust_add2 = models.TextField(default="")
    cust_regi_date = models.DateTimeField(auto_now_add=True,blank=True, null=True) 
    cust_profile = models.ImageField(upload_to="Comp_Profile/",default="",max_length=300,blank=True, null=True)
    cust_pass = models.CharField(default="",max_length=200)

class Company_Product(models.Model):
    comp = models.ForeignKey('Company_data',on_delete=models.CASCADE,blank=True,null=True)
    pro_nm = models.CharField(default="",max_length=200)
    pro_pr = models.PositiveIntegerField(default=0)
    pro_qty = models.PositiveIntegerField(default=0)
    pro_img = models.ImageField(upload_to="ProductPic/",default="",max_length=300,blank=True, null=True)

class Customer_orders(models.Model):
    comp = models.ForeignKey('Company_data',on_delete=models.CASCADE,blank=True,null=True)
    cust = models.ForeignKey('Company_Customer',on_delete=models.CASCADE,blank=True,null=True)
    prod = models.ForeignKey('Company_Product',on_delete=models.CASCADE,blank=True,null=True)
    tot_price = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True,blank=True, null=True) 
    status = models.CharField(default="false",max_length=200)