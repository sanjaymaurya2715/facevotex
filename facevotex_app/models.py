from django.db import models
from django.utils import timezone

# Create your models here.

class Contact(models.Model):
    name= models.CharField(max_length=50,default="")
    email= models.CharField(max_length=100,default="")
    phone=models.CharField(max_length=13,default="")
    query=models.TextField(default="")

    
class Student(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    phone= models.CharField(max_length=50)
    gender = models.CharField(max_length=7)
    city =models.CharField(max_length=30)
    profile_pic =models.ImageField(upload_to="student/profile/")
    address = models.TextField()



class Creator (models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    phone= models.CharField(max_length=50)
    gender = models.CharField(max_length=7)
    organization_name=models.CharField(max_length=60)
    city =models.CharField(max_length=30)
    profile_pic =models.ImageField(upload_to="creator/profile/")
    address = models.TextField()


class Feedback(models.Model):
    voter=models.ForeignKey(Student,on_delete=models.CASCADE)
    rating=models.IntegerField()
    comments=models.TextField()
    submited_on=models.DateField(default=timezone.now)


class Poll(models.Model):
    poll_creator=models.ForeignKey(Creator,on_delete=models.CASCADE)
    tittle=models.CharField(max_length=100)
    description=models.TextField()
    start_date=models.DateField(default=timezone.now) 
    end_date=models.DateField(default=timezone.now) 
    poll_type=models.CharField(max_length=50)
    status=models.CharField(max_length=100, default='not start')


class Candidates(models.Model):
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    candidate_name=models.CharField(max_length=100)
    gender=models.CharField(max_length=50)
    phone= models.CharField(max_length=50)
    age= models.CharField(max_length=50)
    mail= models.CharField(max_length=50)
    votes=models.CharField(max_length=50,default=0)
    profile_pic =models.ImageField(upload_to="candidate/profile/")
    
    
class Vote(models.Model):
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    candidate=models.ForeignKey(Candidates,on_delete=models.CASCADE)
    voter=models.ForeignKey(Student,on_delete=models.CASCADE)
    face=models.ImageField(upload_to='voter_faces/')