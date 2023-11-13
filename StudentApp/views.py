from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from StudentApp.models import Course, City, Student

def login_fun(request):
    if request.method=='POST':
        user_name=request.POST['txtUsername']
        user_pswd=request.POST['txtPassword']
        u1=authenticate(username=user_name,password=user_pswd)#it will return the user object
        if u1 is not None:
            if u1.is_superuser:#checking whether the data is superuser or not
                request.session['Uname']=user_name
                login(request,u1)
                return redirect ('home',)
        else:
            return render(request,'login.html',{'msg':'UserName or Password Incorrect'})

    else:
        return render(request,'login.html')

def register_fun(request):
    if request.method=='POST':
        user_name=request.POST['txtUsername']
        user_pswd=request.POST['txtPassword']
        user_email=request.POST['txtMail']
        if User.objects.filter(username=user_name).exists():
            return render(request,'register.html',{'msg': 'Use Proper User and Password'})
        else:
            u1=User.objects.create_superuser(username=user_name,password=user_pswd,email=user_email)
            u1.save()
            return redirect('log')
    else:#this code will excute when we click hyperlink in login.html page
        return render(request,'register.html')


@login_required
@never_cache
def home_fun(request):
    return render(request,'home.html',{'data':request.session['Uname']})

@login_required
@never_cache
def addcourse_fun(request):
    if request.method=='POST':
        c1=Course()
        c1.course_name=request.POST['txtCourseName']
        c1.course_duration=request.POST['txtCourseDuration']
        c1.course_fees=int(request.POST['txtCourseFees'])
        c1.save()
        return render(request,'addcourse.html',{'msg':'Successfully Added'})
    else:
        return render(request,'addcourse.html')

@login_required
@never_cache
def display_course_fun(request):
    course_data=Course.objects.all()#it will return list of objects
    return render(request,'displaycourse.html',{'data':course_data})

@login_required
@never_cache
def updatecourse_fun(request,courseid):
    c1=Course.objects.get(id=courseid)
    if request.method=='POST':
        c1.course_name=request.POST['txtCourseName']
        c1.course_duration=request.POST['txtCourseDuration']
        c1.course_fees=int(request.POST['txtCourseFees'])
        c1.save()
        return redirect('display_course')
    else:
        return render(request,'updatecourse.html',{'data':c1})

@login_required
@never_cache
def deletecourse_fun(request,courseid):
    c1=Course.objects.get(id=courseid)
    c1.delete()
    return redirect('display_course')

@login_required
@never_cache
def addstudent_fun(request):
    if request.method=="POST":
        s1=Student()
        s1.stud_name=request.POST["txtName"]
        s1.stud_phno=request.POST["txtPhno"]
        s1.stud_email=request.POST["txtMail"]
        s1.stud_city=City.objects.get(city_name=request.POST['ddlCity'])
        s1.stud_course=Course.objects.get(course_name=request.POST['ddlCourse'])
        s1.paid_fees=int(request.POST["txtPaidFees"])
        c1=Course.objects.get(course_name=request.POST['ddlCourse'])
        s1.pending_fees=c1.course_fees-s1.paid_fees
        s1.save()
        return redirect('addstudent')
    else:
        city=City.objects.all
        course=Course.objects.all()
        return render(request,'addstudent.html',{'CityData':city,'CourseData':course})

@login_required
@never_cache
def displaystudent_fun(request):
    s1=Student.objects.all()
    return render(request,'displaystudent.html',{'studentdata':s1})

@login_required
@never_cache
def updatestudent_fun(request, stud_id):
    s1 = Student.objects.get(id=stud_id)

    if request.method == "POST":
        # Get the values from the form
        paid_fees = int(request.POST["txtPaidFees"])
        # Calculate the new pending fees based on the paid fees
        pending_fees = s1.pending_fees - paid_fees
        pending_fees = max(pending_fees, 0)  # Make sure pending fees doesn't go below 0

        # Update the student's information
        s1.stud_name = request.POST["txtName"]
        s1.stud_phno = request.POST["txtPhno"]
        s1.stud_email = request.POST["txtMail"]
        s1.stud_city = City.objects.get(city_name=request.POST['ddlCity'])
        s1.stud_course = Course.objects.get(course_name=request.POST['ddlCourse'])
        s1.paid_fees += paid_fees
        s1.pending_fees = pending_fees
        s1.save()

        return redirect('displaystudent')
    else:
        city = City.objects.all()
        course = Course.objects.all()
        return render(request, 'updatestudent.html', {'student': s1, 'CityData': city, 'CourseData': course})

@login_required
@never_cache
def deletestudent_fun(request,stud_id):
    s1=Student.objects.get(id=stud_id)
    s1.delete()
    return redirect('displaystudent')

def logout_fun(request):
    logout(request)
    return redirect('log')
