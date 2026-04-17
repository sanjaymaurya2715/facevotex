from django.shortcuts import render, redirect, get_object_or_404
from. models import Student, Feedback, Poll, Candidates, Vote
from django.contrib import messages

from .utils import match_faces

def register (request):
    if request.method=='GET':
     return render(request,"facevotex_app/voter/voter_registation.html")
    if request.method=='POST':
       name=request.POST["name"]
       email = request.POST["email"]
       phone = request.POST["phone"]
       password = request.POST["password"]
       gender=request.POST['gender']
       city=request.POST['city']
       address=request.POST['address']
       profile_pic=request.FILES['profile_image']
       
       print(name,email,phone,password,gender,city,address,profile_pic,)
       Student_obj=Student(name=name,email=email,phone=phone,password=password,gender=gender,city=city,address=address,profile_pic=profile_pic,)
       Student_obj.save()
       messages.success(request,"welcome to the jungle...........")
       return render(request,"facevotex_app/voter/voter_registation.html")
    

def voter_home(request):
   key=request.session.keys()
   if "role" in key:
      if request.session["role"]=="voter":
                         if request.method=="GET":
                              email=request.session["email"]
                              v_obj=Student.objects.get(email=email)
                              voter_info={
                                    "voter":v_obj
                              }
                              return render(request,'facevotex_app/voter/voter_homepage.html',voter_info)
                         if request.method=='POST':
                              pass
   else:
          messages.error(request,"unauthorized access")
          return redirect("login")
                         
def voter_home_edit(request):
   key=request.session.keys()
   if "role" in key:
      if request.session["role"]=="voter":
                         if request.method=="GET":
                              email=request.session["email"]
                              v_obj=Student.objects.get(email=email)
                              voter_info={
                                    "voter":v_obj
                              }
                              return render(request,'facevotex_app/voter/voter_home_edit.html',voter_info)
                         if request.method=='POST':
                              email=request.session["email"]
                              s_obj=Student.objects.get(email=email)
                              s_obj.name=request.POST["name"]
                              s_obj.phone=request.POST["phone"]
                              if "profile_pic" in request.FILES:
                                   s_obj.profile_pic=request.FILES["profile_pic"]
                              s_obj.save()
                              messages.success(request,"profile edit success....")
                              return redirect("voter_home_edit")  



def login(request):

      if request.method=='GET':
            return render(request,'facevotex_app/voter/login.html')
     
      if request.method=='POST':
            v_email=request.POST["email"]
            v_password=request.POST["password"]
            data=Student.objects.filter(email=v_email)
            if len(data)>0:
                  if v_password==data[0].password:
                        request.session["role"]="voter" 
                        request.session["email"]=v_email
                        return redirect("voter_home")
                  else:
                        return redirect('login')



def feedback (request):
   
   key=request.session.keys()
   if"role"in key:
      if request.session["role"]=="voter":
                         if request.method=="GET":
                              return render(request,'facevotex_app/voter/feedback.html')
                         if request.method=='POST':
                              voter_email=request.session['email']
                              Student_obj=Student.objects.get(email=voter_email)
                              rating=request.POST["rating"]
                              messages=request.POST['message']
                              print(voter_email,rating,messages)
                              feedback_obj=Feedback(voter=Student_obj,rating=rating,comments=messages)
                              feedback_obj.save()
                              messages.success(request,"feedback successfully saved")
                              return render(request,'facevotex_app/voter/feedback.html')
                              

def voter_view_polls(request):
      
                  poll_obj = Poll.objects.all()
                  data={
                       "polls":poll_obj 
                  }
                  
                      
                  return render(request,'facevotex_app/voter/voter_views_poll.html',data)                       


def voter_view_candidate(request,id):
                  if request.method=='GET':
                    poll = Poll.objects.get(id=id)
                    ca_obj = Candidates.objects.filter(poll=poll)
                    data={
                       "info":ca_obj
                    }
                  
                    return render(request,'facevotex_app/voter/voter_view_candidate.html',data)  


def voting(r,pid):
              candidate=Candidates.objects.get(id=pid)
              
              voter=Student.objects.get(email=r.session['email'])

              if candidate.poll.poll_type=='restricted':
                     messages.error(r,"restricted poll.....")
                     return redirect("voter_home")              
              if Vote.objects.filter(poll=candidate.poll,voter=voter).exists():
                     messages.error(r,"already voted.....")
                     return redirect("voter_home")
              if candidate.poll.status=="not start":
                     messages.error(r,"poll voting not started yet")
                     return redirect("voter_view_poll")
              if candidate.poll.status=="ended":
                     messages.error(r,"poll voting has been ended.")
                     return redirect("voter_view_poll")
                     
              

                     
              if r.method=="POST":       
                    candidate=Candidates.objects.get(id=pid)
                    v=Vote.objects.create(
                         poll=candidate.poll,
                         candidate=candidate,
                         voter=voter,
                         face=r.FILES['face']
                    )
                    candidate.votes=int(candidate.votes)+1
                    candidate.save()
                    if not match_faces(voter.profile_pic.path,v.face.path):
                         v.delete()
                         messages.error(r,"face not matched")
                         return redirect('voter_home')
                         
                    return redirect('/result/'+str(candidate.poll.id))

              return render(r,'facevotex_app/voter/voting.html',{
                         'poll':candidate.poll,
                         'candidate':Candidates.objects.filter(poll=candidate.poll)
                    })    
               

def result(request, pid):
    if "role" not in request.session or request.session.get("role") != "voter":
        messages.error(request, "Please log in to view results.")
        return redirect("login")

    voter = get_object_or_404(Student, email=request.session.get("email"))
    poll = get_object_or_404(Poll, id=pid)
    vote = Vote.objects.filter(poll=poll, voter=voter).order_by('-id').first()
    candidate = vote.candidate if vote else None
    message = "Your vote has been submitted successfully." if candidate else "No vote record found for this poll."

    return render(request, "facevotex_app/voter/result.html", {
        "poll": poll,
        "candidate": candidate,
        "message": message,
    })


def camera_view(request):
    return render(request, 'facevotex_app/voter/camera.html')


