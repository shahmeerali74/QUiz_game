from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import mysql.connector as mysql
from django.contrib.auth.hashers import make_password, check_password

def login_required(view_func):
    # @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect('login')  # Redirect to login if user is not logged in
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def index(request):
    username=request.session.get('username')
    return render(request,'home.html',{'username':username})

@login_required
def about(request):
    return render(request, 'aboutus.html')

@login_required
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
            cursor.execute(""" SELECT * FROM users WHERE email = %s """,(email,))
            user=cursor.fetchone()
            if user:
                hashed_password=user[3]
                print(hashed_password)
                if check_password(password,hashed_password):
                    userid=user[0]
                    username=user[1]

                    request.session['user_id']=userid
                    request.session['username']=username
                    # return render(request,'home.html',{'username':username})
                    return redirect ('index')
                else:
                    return render(request, 'login.html', {'login_error': 'Invalid email or password'}) 
            else:
                return render(request,'signup.html',{'notLoginErr':'you dont have an account'})
        except mysql.Error as err:
            print  (f"ERROR: {err}")
            return render(request,'signup.html',{'db_connection_err':'db is not connected'})
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
            return redirect('login')
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
    hashed_password= make_password(password)
    print("Hashed Password:", hashed_password)
    cursor.execute("""
         INSERT INTO users (name, email, password) VALUES (%s, %s, %s)
    """, (name, email, hashed_password))

    db.commit()




def signout(request):
    request.session.clear()
    return redirect('login')