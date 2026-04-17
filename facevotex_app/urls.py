from django.urls import path
from . import views 
from . import voter_views,creator_views

urlpatterns =[
    path("",views.home,name="home"),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name='contact'),
    path("voter_registation/",voter_views.register,name='voter_registation'),
    path("creator_register/",creator_views.creator_register,name='creator_register'),
    path("voter_feedback/",voter_views.feedback,name='voter_feedback'),
    path("login/",voter_views.login,name='login'),
     path("v_home/",voter_views.voter_home,name="voter_home"),
    path("c_login/",creator_views.c_login,name='c_login'),
    path("creator_home/",creator_views.creator_home,name='creator_home'),
    path("create_poll/",creator_views.poll_makeing,),
    path("view_poll/",creator_views.view_polls,name='view_polls'),
    path("add_candidate/<str:id>/",creator_views.candidate_adding),
    path("save_candidate/",creator_views.save_candidate),
    path("camera/",voter_views.camera_view,),
    path("logout/",views.logout,name="logout"),
    path("creator_edit_profile/",creator_views.edit_profile,name="creator_edit_profile"),
    path("voter_view_poll/",voter_views.voter_view_polls,name='voter_view_poll'),
    path("voter_home_edit/",voter_views.voter_home_edit,name='voter_home_edit'),
    path("voter_view_candidate/<str:id>/",voter_views.voter_view_candidate,name='voter_view_candidate'),
    path("voting/<str:pid>/",voter_views.voting,name="voting"),
    path('result/<int:pid>/',voter_views.result),
    path('view_candidate/<str:id>/',creator_views.view_candidate,name='view_candidate'),
    path('update_status/<str:id>/<str:task>/',creator_views.update_status,name='update_status'),
    path('view_result/<str:id>/',creator_views.view_result,name='view_result'),
   


]