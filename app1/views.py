from django.shortcuts import render, redirect
from .models import Company_data, Customer_orders,Company_Customer, Company_Product
from django.http import HttpResponse
# Create your views here.


import smtplib
import random
import email.message
# ------------------------- company ---------------------------

def Company_login(request):
    if request.POST:
        em = request.POST['email']
        ps = request.POST['pass']
        
        try:
            var = Company_data.objects.get(com_em = em)
            print(var)
            if var.com_pass == ps:
                request.session['comp_data'] = var.id
                return redirect('ComDashBoard')
            else:
                return HttpResponse("<h1><a href=""> You Have Entered Wrong Password ... </a></h1>")
        except:
            return HttpResponse("<h1><a href=""> You Have Entered Wrong Email Id </a></h1>")
            
    return render(request,'company/login/login.html')

def Company_regi(request):
    if request.POST:
        nm = request.POST['name']
        em = request.POST['email']
        pass1 = request.POST['pass']
        pass2 = request.POST['re_pass']
        
        try:
            var = Company_data.objects.get(com_em = em)
            return HttpResponse("<h1><a href=""> Email Id Already Registered... </a></h1>")
        except:
            if pass1 == pass2:
                obj = Company_data()
                obj.com_name = nm
                obj.com_em = em
                obj.com_pass = pass2
                obj.save()
                return redirect('c_login')
            else:
                return HttpResponse("<h1><a href=""> Passwords are Not Match </a></h1>")
        
    return render(request,'company/login/regi.html')

def CompForgetPass(request):
    if request.POST:
        em1 = request.POST['em']
        print(em1)
        try:
            valid = Company_data.objects.get(com_em = em1)
            print(valid)
            
            sender_email = 'darpansalunkework@gmail.com'
            sender_pass = 'Darpan@work'
            reciv_email = em1
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            
            # OTP --------------
            nos = [1,2,3,4,5,6,7,8,9,0]
            otp = ""
            for i in range(4):
                otp += str(random.choice(nos))
                print(otp)
            print(otp)
            
            mes1 = f"""
            This Is Your OTP
            {otp}
            
            
            
            Don't share With Others......
            """
            
            msg = email.message.Message()
            msg['Subject'] = "OTP From This Site"
            msg['From'] = sender_email
            msg['To'] = reciv_email
            password = sender_pass
            msg.add_header('Content-Type','text/html')
            msg.set_payload(mes1)   
            
            server.starttls()
            server.login(msg['From'],password)
            server.sendmail(msg['From'],msg['To'],msg.as_string())
                     
            request.session['otp'] = otp
            
            request.session['new_user'] = valid.id
            return redirect('OTP_check')
        except:
            return HttpResponse('<a href=""> You Have Entered Wrong Email Id... </a>')
    return render(request,'company/login/Forget_pass.html')

def OTP_check(request):
    if 'otp' in request.session.keys():
        print("New OTP check")
        if request.POST:
            ot1 = request.POST['ot1']
            print(ot1)
            otp = request.session['otp']
            print(otp)
            if ot1 == otp:
                del request.session['otp']
                print("You Are Ready For Create New Password...")
                return redirect('New_Password')
            else:
                del request.session['otp']
                return redirect('CompForgetPass')
        return render(request,'company/login/OTP_CHECK.html')
    else:
        return redirect('c_login')

def New_Password(request):
    if 'new_user' in request.session.keys():
        if request.POST:
            p1 = request.POST['pass1']
            p2 = request.POST['pass2']
            print(p1,p2)
            if p1 == p2:
                obj = Company_data.objects.get(id = int(request.session['new_user']))
                obj.com_pass = p2
                obj.save()
                del request.session['new_user']
                return redirect('c_login')
            else:
                return HttpResponse('<a href=""> Both Passwords Are Not Same </a>')
        return render(request,'company/login/NewPass1.html')
    else:
        return redirect('c_login')

def ComDashBoard(req):
    if 'comp_data' in req.session.keys():
        User = Company_data.objects.get(id = int(req.session['comp_data']))
        return render(req,'company/dash/index.html',{'USERS':User})
    else:
        return redirect('c_login')

def Profile_Manage(req):
    if 'comp_data' in req.session.keys():
        User = Company_data.objects.get(id = int(req.session['comp_data']))
        
        if req.POST:
            nm = req.POST['nm1']
            em = req.POST['em1']
            add1 = req.POST['add1'] 
            con = req.POST['con1']
            pass1 = req.POST['pass1']
            img1 = req.FILES.get('img1')
            
            User.com_name = nm
            User.com_em = em
            User.com_cno = con
            User.com_add = add1
            User.com_pass = pass1
            print(img1)
            if img1 != None:
                User.profile = img1
            User.save()
            
        return render(req,'company/dash/Profile.html',{'USERS':User})
    else:
        return redirect('c_login')

def AddCompCustomer(req):
    if 'comp_data' in req.session.keys():
        User = Company_data.objects.get(id = int(req.session['comp_data']))
        if req.POST:
            nm = req.POST['nm1']
            em = req.POST['em1']
            con = req.POST['con1']
            
            obj = Company_Customer()
            obj.comp = User
            obj.cust_nm = nm
            obj.cust_em = em
            obj.cust_con = con
            
            # Password Create --------------
            salfa = 'qwertyuiopasdfghjklzxcvbnm'
            ualfa = salfa.upper()
            spic = '!@#$%^&*()'
            num = '1234567890'
            data = salfa + ualfa + spic + num
            otp = ""
            for i in range(8):
                otp += str(random.choice(data))
                print(otp)
            print(otp)
            
            obj.cust_pass = otp
            obj.save()
            
            try:
                sender_email = 'darpansalunkework@gmail.com'
                sender_pass = 'Darpan@work'
                reciv_email = em
                
                server = smtplib.SMTP('smtp.gmail.com',587)
                
                
                mes1 = f"""
                Hello, 
                Your Now New Customer Of This company, 
                Here is Your Login Details 
                
                email id = {em}
                password = {otp}
                link = http://127.0.0.1:8000/Customer_Login/
                
                
                """
                
                msg = email.message.Message()
                msg['Subject'] = "New Customer Added"
                msg['From'] = sender_email
                msg['To'] = reciv_email
                password = sender_pass
                msg.add_header('Content-Type','text/html')
                msg.set_payload(mes1)   
                
                server.starttls()
                server.login(msg['From'],password)
                server.sendmail(msg['From'],msg['To'],msg.as_string())
                return redirect('ViewCustomer')
            except:
                return HttpResponse('<a href=""> You Have Entered Wrong Email Id... </a>')
        return render(req,'company/dash/add_Customer.html',{'USERS':User})
    else:
        return redirect('c_login')

def ViewCustomer(request):
    if 'comp_data' in request.session.keys():
        User = Company_data.objects.get(id = int(request.session['comp_data']))
        custs = Company_Customer.objects.filter(comp = User)
        return render(request,'company/dash/view_Customer.html',{'USERS':User,'cust':custs})
    else:
        return redirect('c_login')
    
def DeleteCustomer(request,id):
    if 'comp_data' in request.session.keys():
        custs = Company_Customer.objects.get(id=id)
        custs.delete()
        # print(custs)
        return redirect('ViewCustomer')
    else:
        return redirect('c_login')

def Vieworder(req):
    if 'comp_data' in req.session.keys():
        User = Company_data.objects.get(id = int(req.session['comp_data']))
        cord = Customer_orders.objects.filter(comp=User,status="false")
        return render(req,'company/dash/vieworder.html',{'USERS':User,'cord':cord})
    else:
        return redirect('c_login')

def YESorder(req,id):
    if 'comp_data' in req.session.keys():
     
        cord = Customer_orders.objects.get(id=id)
        cord.status = "yes"
        cord.save()
        return redirect('vieworder')
    else:
        return redirect('c_login')

def NOorder(req,id):
    if 'comp_data' in req.session.keys():
        cord = Customer_orders.objects.get(id=id)
        cord.status = "no"
        cord.save()
        return redirect('vieworder') 
    else:
        return redirect('c_login')



def Logout_Comp(request):
    if 'comp_data' in request.session.keys():
        del request.session['comp_data']
        return redirect('c_login')
    else:
        return redirect('c_login')

# ------------------------- company ---------------------------

# ------------------------- product --------------------------

def AddProduct(req):
    if 'comp_data' in req.session.keys():
        User = Company_data.objects.get(id = int(req.session['comp_data']))
        if req.POST:
            nm = req.POST['nm1']
            pr = req.POST['pr1']
            qty = req.POST['qty1']
            img = req.FILES.get('img1')
            
            var = Company_Product()
            var.comp = User
            var.pro_nm = nm
            var.pro_pr = pr
            var.pro_qty = qty
            var.pro_img = img
            var.save()
            
            return redirect('ViewProduct')
        return render(req,'company/dash/add_Product.html',{'USERS':User})
    else:
        return redirect('c_login')

def UpdateProduct(req,id):
    if 'comp_data' in req.session.keys():
        User = Company_data.objects.get(id = int(req.session['comp_data']))
        prod = Company_Product.objects.get(id = id)
        if req.POST:
            nm = req.POST['nm1']
            pr = req.POST['pr1']
            qty = req.POST['qty1']
            img = req.FILES.get('img1')
            
            prod.comp = User
            prod.pro_nm = nm
            prod.pro_pr = pr
            prod.pro_qty = qty
            if img != None:
                prod.pro_img = img
            prod.save()
            
            return redirect('ViewProduct')
        return render(req,'company/dash/update_Product.html',{'USERS':User,'prod':prod})
    else:
        return redirect('c_login')

def ViewProduct(req):
    if 'comp_data' in req.session.keys():
        User = Company_data.objects.get(id = int(req.session['comp_data']))
        prod = Company_Product.objects.filter(comp=User)
        return render(req,'company/dash/view_Product.html',{'USERS':User,'prod':prod})
    else:
        return redirect('c_login')
    
def DeleteProduct(req,id):
    if 'comp_data' in req.session.keys():
        prod = Company_Product.objects.get(id = id)
        prod.delete()
        return redirect('ViewProduct')
    else:
        return redirect('c_login')


# ------------------------- product ---------------------------

# ------------------------- Customer ---------------------------

def Customer_Login(request):
    if request.POST:
        em = request.POST['email']
        ps = request.POST['pass']
        
        try:
            valid = Company_Customer.objects.get(cust_em = em, cust_pass = ps)
            request.session['custom_user'] = valid.id
            return redirect('Customer_dash')
        except:
            return redirect('Customer_Login')
    return render(request,'customer/login/login.html')

def Customer_dash(request):
    if 'custom_user' in request.session.keys():
        cust = Company_Customer.objects.get(id = int(request.session['custom_user']))
        prod = Company_Product.objects.filter(comp = cust.comp)
        return render(request,'customer/dash/index.html',{'prod':prod})
    else:
        return redirect('Customer_Login')

def Customer_order(request):
    if 'custom_user' in request.session.keys():
        cust = Company_Customer.objects.get(id = int(request.session['custom_user']))
        ord = Customer_orders.objects.filter(cust = cust)
        return render(request,'customer/dash/order.html',{'ord':ord})
    else:
        return redirect('Customer_Login')

def Profile(request):
    if 'custom_user' in request.session.keys():
        cust = Company_Customer.objects.get(id = int(request.session['custom_user']))
        if request.POST:
            nm = request.POST['nm']
            em = request.POST['em']
            cno = request.POST['con']
            pa1 = request.POST['pass']
            add1 = request.POST['ad1']
            add2 = request.POST['ad2']
            img1 = request.FILES.get('img1')
            
            cust.cust_nm = nm
            cust.cust_em = em
            cust.cust_con = cno
            cust.cust_add1 = add1
            cust.cust_add2 = add2
            cust.cust_pass = pa1
            if img1 != None:
                cust.cust_profile = img1
            cust.save()
            
        return render(request,'customer/dash/profile.html',{'cust':cust})
    else:
        return redirect('Customer_Login')

def order_place(request,id):
    if 'custom_user' in request.session.keys():
        cust = Company_Customer.objects.get(id = int(request.session['custom_user']))
        prod = Company_Product.objects.get(id = id)
        if request.POST:
            qty1 = request.POST['qty1']
            obj = Customer_orders()
            obj.comp = cust.comp
            obj.cust = cust
            obj.prod = prod
            obj.qty = int(qty1)
            obj.tot_price = int(int(qty1) * int(prod.pro_pr))
            obj.save()
            return redirect('Customer_dash')
        return render(request,'customer/dash/order_place.html',{'prod':prod})
    else:
        return redirect('Customer_Login')

def Customer_logout(request):
    if 'custom_user' in request.session.keys():
        del request.session['custom_user']
        return redirect('Customer_Login')
    else:
        return redirect('Customer_Login')

# ------------------------- Customer ---------------------------


