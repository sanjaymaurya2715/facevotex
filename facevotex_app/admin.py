from django.contrib import admin

# Register your models here.
from . models import Student, Contact , Feedback ,Poll, Candidates, Creator, Vote

admin.site.register(Student)
admin.site.register(Contact)
admin.site.register(Feedback)
admin.site.register(Creator)
admin.site.register(Candidates)
admin.site.register(Poll)
admin.site.register(Vote)
