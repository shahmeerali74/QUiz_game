from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import mysql.connector as mysql
def index(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'aboutus.html')

def game(request):
        
    # api_url="https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=multiple"
    # questions=requests.get(api_url).json().get('results',[])
    return render(request, 'game.html')
# ,{'questions':questions}

def login (request):
    if request.method=='POST':
        email=request.POST.get("email")
        password=request.POST.get("password")

        try:
            db=mysql.connect(
                host='localhost',
                user='root',
                password="",
                database="loginqzgame"
            )
            cursor=db.cursor()
            cursor.execute(""" SELECT * FROM users WHERE email = %s AND password = %s """,(email,password))
            user=cursor.fetchone()
            if user:
                userid=user[0]
                username=user[1]

                request.session['user_id']=userid
                request.session['username']=username
                return render(request,'home.html',{'username':username})
            
            else:
                return HttpResponse("not successfull")
        except mysql.Error as err:
            print  (f"ERROR: {err}")
            return HttpResponse("error occured login db")
    else:    
        return render(request, 'login.html')













def signup(request):
    if request.method=='POST':
        name= request.POST.get('name')
        email=request.POST.get('email')
        password= request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')

        if not name or not email or not password or not confirm_password:
            return render(request,'signup.html',{'notFillErr':'please fill all the fields'})

        if password != confirm_password:
            return render(request,'signup.html',{'pass_err':'password and cpassword dont match'})
        
        print ("recived:", name,email,password)
        try:
            db=mysql.connect(
                host="localhost",
                user="root",
                password="",
                database="loginqzgame"
            )
            cursor=db.cursor()

            signup_user(name,email,password,cursor,db)
        except mysql.Error as err:
            if err.errno == 1062:
                return render(request, 'signup.html', {'email_error':'Email already exist choose different one!'})
            else:
                return HttpResponse(f"ERROOR: {err}")
            # if err.errno == 1062:
            #     return render(request, 'signup.html',{'error_email':'Email already exist choose different one!'})
            # return HttpResponse(f"ERROR: {err}")
    return render(request, 'signup.html')


def signup_user(name, email, password, cursor, db):
    cursor.execute("""
         INSERT INTO users (name, email, password) VALUES (%s, %s, %s)
    """, (name, email, password))

    db.commit()




def signout(request):
    request.session.clear()
    return redirect('login')