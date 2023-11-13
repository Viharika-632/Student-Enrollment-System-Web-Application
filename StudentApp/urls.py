from django.urls import path

from StudentApp import views

urlpatterns = [
    path('',views.login_fun,name='log'),
    path('reg',views.register_fun,name='reg'),# it will redirected to register.html page
    path('home',views.home_fun,name='home'),#it will redirect to home.html page
    path('add_course',views.addcourse_fun,name='add_course'),#it will redirecting to addcourse.html page
                                                          #inserting course data
    path('display_course',views.display_course_fun,name='display_course'),#it will collect the data from course table
                                                                       # and send to displaycourse.html page
    path('update_course/<int:courseid>',views.updatecourse_fun,name='update_course'),
    path('delete_course/<int:courseid>',views.deletecourse_fun,name='delete_course'),
    path('addstudent',views.addstudent_fun,name='addstudent'),
    path('displaystudent',views.displaystudent_fun,name='displaystudent'),
    path('updatestudent/<int:stud_id>',views.updatestudent_fun,name='updatestudent'),
    path('deletestudent/<int:stud_id>',views.deletestudent_fun,name='deletestudent'),
    path('logout',views.logout_fun,name='logout'),
]
