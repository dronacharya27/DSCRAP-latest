from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact
from .models import Useraddress
from .models import MyUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import docform
from .obj import objd
from datetime import datetime
import pandas as pd
from django.conf import settings
import os
from .apps import user_directory_path
from IPython.display import HTML

# CONTACT

def index(request):
    return render(request,'index.html')

def contact2(request):
    if request.method == "POST":
        Name= request.POST.get('name','')
        Email= request.POST.get('email','')
        Subject = request.POST.get('subject','')
        Message= request.POST.get('message','')

    contact = Contact(name=Name,email=Email,subject= Subject,message =Message)
    contact.save()
    messages.success(request,"Your Message Has been sent successfully")
    return redirect('index')

# LOGIN

def handlelogin(request):
    
    if request.method == "POST":
        
        loginname = request.POST["email"]
        loginpass = request.POST.get('loginpass','')

        user = authenticate(request,email=loginname, password=loginpass)
        print(f"Authenticated user: {user}")
        if user is not None:
            print(f"Authenticated user: {user}")
            login(request,user)
            messages.success(request,'Successfully Logged In')
            return redirect('index')

        else:
            messages.error(request,'Invalid Credentials, Please Try Again!')
            return redirect('index')
    else:
        return HttpResponse('404-Not Found')
    
def handlelogout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request,"Successfully Loged-Out")
        return redirect('index')

    return HttpResponse('handlelogout')


# SIGNUP

def handlesignup(request):

    if request.method == "POST":
        postdata = request.POST.copy()
        username = postdata.get('username', '')
        email = postdata.get('email', '')
        password = postdata.get('passw', '')
        
        existing_user = MyUser.objects.filter(email=email).first()
        if(existing_user):
            messages.error(request,"User Already Exist")
            return redirect('index')
        create_new_user = MyUser.objects.create_user(email=email, password=password, username=username)
        create_new_user.is_active = True
        create_new_user.is_admin = True
        create_new_user.save()
    
        login(request, create_new_user)
        if create_new_user is not None:
                if create_new_user.is_active:
                    messages.success(request,"USER CREATED SUCCESFULLY")
                    return redirect('index')
                else:
                    print("The password is valid, but the account has been disabled!")


    return  redirect('index')
# UPLOAD AND BACKEND

def trye(request):
    if request.method == "POST":
        form = docform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            date = datetime.now()
            name = date.strftime('%H%M')
            document_instance = form.instance
            if document_instance.image:
                _, extension = os.path.splitext(document_instance.image.name)
            else:
                extension = None
            print(f"Uploaded file extension: {extension}")
            path = settings.DETECT_ROOT+f'/scrap{name}{extension}'
            detect = objd(path)
            options = detect[0]
            final = detect[1]

            # Check if the lengths of options and final are the same
            if len(options) != len(final):
                messages.error(request, "Invalid data received. Please try again.")
                return redirect('scr')

            total = detect[2]
            no_items = detect[3]

            df = pd.DataFrame({"ITEMS": options, "PRICES": final})
            html = df.to_html(classes=["table-bordered", "table-primary", "table-hover", "table-l"])

            text_file = open("./main/templates/table.html", "w")
            text_file.write(html)
            text_file.close()

            params = {'final': final, 'options': options, 'total': total, 'no_items': no_items}
            return render(request, 'bill.html', params)
        else:
            context = {'form': form}
            messages.success(request, "Uploaded Successfully")
            return render(request, 'scrapcalc.html', context)

    context = {'form': docform()}
    return render(request, 'scrapcalc.html', context)


def address(request):
    if request.method=="POST":
        name = request.POST.get('aname','')
        address = request.POST.get('add','')
        address = Useraddress(name,address)
    address.save()
    messages.success(request,"Pick-Up Set Successfully!")
    return redirect('index')
   




