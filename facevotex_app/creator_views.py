from django.shortcuts import render, redirect
from. models import Creator,Poll,Candidates
from django.contrib import messages
poll_id=0
def creator_register (request):
    if request.method=='GET':
     return render(request,"facevotex_app/poll_creator/creator_register.html")
    if request.method=='POST':
       name= request.POST["name"]
       email = request.POST["email"]
       phone = request.POST["phone"]
       password = request.POST["password"]
       gender=request.POST['gender']
       city= request.POST["city"]
       organization_name=request.POST['organization_name']
       
       address=request.POST['address']
       profile_pic=request.FILES['profile_picture']
       
       print(name,email,phone,password,gender,organization_name,city,address,profile_pic,)
       Creator_obj=Creator(name=name,email=email,phone=phone,password=password,gender=gender,organization_name=organization_name,city=city,address=address,profile_pic=profile_pic,)
       Creator_obj.save()
       messages.success(request,"")
       return render(request,"facevotex_app/poll_creator/creator_register.html")
    

def creator_home(request):
   key=request.session.keys()
   if "role" in key:
      if request.session["role"]=="creator":
                         if request.method=="GET":
                              email=request.session["email"]
                              C_obj=Creator.objects.get(email=email)
                              creator_info={
                                    "creator":C_obj
                              }
                              return render(request,'facevotex_app/poll_creator/creator_home.html',creator_info)
                           
def edit_profile(request):
     key=request.session.keys()
     if "role" in key:
            if request.session["role"]=="creator":
                              if request.method=="GET":
                                    email=request.session["email"]
                                    C_obj=Creator.objects.get(email=email)
                                    creator_info={
                                          "creator":C_obj
                                    }
                                    return render(request,'facevotex_app/poll_creator/creator_edit_profile.html',creator_info)
                              if request.method=="POST":
                                   email=request.session["email"]
                                   c_obj=Creator.objects.get(email=email)
                                   c_obj.name=request.POST["name"]
                                   c_obj.phone=request.POST["phone"]
                                   c_obj.profile_pic=request.FILES["profile_picture"]
                                   c_obj.save()
                                   messages.success(request,"profile edit success....")
                                   return redirect("creator_edit_profile")

                                   
                                   
     

def c_login(request):
      if request.method=='GET':
            return render(request,'facevotex_app/poll_creator/creator_login.html')
     
      if request.method=='POST':
            c_email=request.POST["email"]
            c_password=request.POST["password"]
            data=Creator.objects.filter(email=c_email)
            if len(data)>0:
                  if c_password==data[0].password:
                        request.session["role"]="creator" 
                        request.session["email"]=c_email
                        return redirect('creator_home')
                  else:
                        return redirect('login')
                  

def poll_makeing(request):
    if request.method=='GET':
     return render(request,"facevotex_app/poll_creator/creation.html")
    if request.method=='POST':
       email= request.session["email"]
       Creator_obj=Creator.objects.get(email=email)
       tittle = request.POST["tittle"]
       start_date = request.POST["start_date"]
       end_date = request.POST["end_date"]
       poll_type=request.POST['poll_type']
       description= request.POST["description"]
       
       print(tittle,start_date,end_date,poll_type,description)
       Poll_obj=Poll(poll_creator=Creator_obj,tittle=tittle,start_date=start_date,end_date=end_date,poll_type=poll_type,description=description)
       Poll_obj.save()
       messages.success(request,"")
       return redirect('creator_home')   


def view_polls(request):
      key=request.session.keys()
      if "role" in key:
         if request.session["role"]=="creator":
             if request.method=='GET':
                  email=request.session["email"]
                  creator_obj=Creator.objects.get(email=email)
                  poll_obj = Poll.objects.filter(poll_creator=creator_obj)
                  data={
                       "polls":poll_obj 
                  }
                  
                      
                  return render(request,'facevotex_app/poll_creator/view_polls.html',data)
             



def candidate_adding(request,id):
     if request.method=='GET':
      global poll_id
      poll_id=id
      return render(request,"facevotex_app/poll_creator/add_candidate.html")
     

def save_candidate(request):  
      if request.method=='POST':
        print(poll_id)
        poll = Poll.objects.get(id=poll_id)
        
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        age = request.POST["age"]
        gender=request.POST['gender']
        profile_pic=request.FILES['profile_picture']
        Candidates_obj=Candidates(poll=poll,candidate_name=name,mail=email,phone=phone,age=age,gender=gender,profile_pic=profile_pic,)
        Candidates_obj.save()
        messages.success(request,"")
        return redirect('view_polls')
                 

def view_candidate(request,id):
                  if request.method=='GET':
                    poll = Poll.objects.get(id=id)
                    ca_obj = Candidates.objects.filter(poll=poll)
                    data={
                       "info":ca_obj
                    }
                  
                    return render(request,'facevotex_app/poll_creator/view_candidate.html',data)  

             
                        
def update_status (request,id,task):
            poll=Poll.objects.get(id=id)
            poll.status=task
            poll.save()
            messages.success(request,'the poll is updated')
            return redirect('view_polls')

            
def view_result(request,id):
                  if request.method=='GET':
                    poll = Poll.objects.get(id=id)
                    ca_obj = Candidates.objects.filter(poll=poll)

                    candidate_votes = []
                    for candidate in ca_obj:
                        try:
                            votes = int(candidate.votes)
                        except (TypeError, ValueError):
                            votes = 0
                        candidate_votes.append((candidate, votes))

                    if candidate_votes:
                        max_votes = max(votes for _, votes in candidate_votes)
                        winner_names = [candidate.candidate_name for candidate, votes in candidate_votes if votes == max_votes]
                    else:
                        max_votes = 0
                        winner_names = []

                    data = {
                       "info": ca_obj,
                       "winner_names": winner_names,
                       "winner_votes": max_votes,
                       "winner_heading": "Winner" if len(winner_names) == 1 else "Winners"
                    }
                                                        
                    return render(request,'facevotex_app/poll_creator/view_result.html',data)            