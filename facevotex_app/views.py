from django.shortcuts import render,redirect
from. models import Contact

# Create your views here.
def home(request):
    return render(request,"facevotex_app/html/index.html")

def about (request):
    return render(request,"facevotex_app/html/about.html")

def contact (request):
    if request.method=='GET':
       return render(request,"facevotex_app/html/contact.html")    
    if request.method=='POST':
        name =request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        query= request.POST["message"]
        print('name=',name,"email=",email,'phone=',phone,'message=',query)
        contact_obj =contact(name=name, email=email, phone=phone, query=query)
        contact_obj.save()

        return render(request,"facevotex_app/html/contact.html")


def logout(request):
     request.session.delete()
     return redirect("home")