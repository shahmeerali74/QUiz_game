from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
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
    return render(request, 'login.html')






def signup(request):
    if request.method=='POST':
        name= request.POST.get('name')
        email=request.POST.get('email')
        password= request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse("Password and confirm password do not match")
        
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
            return HttpResponse(f"ERROR: {err}")
    return render(request, 'signup.html')


def signup_user(name, email, password, cursor, db):
    cursor.execute("""
         INSERT INTO users (name, email, password) VALUES (%s, %s, %s)
    """, (name, email, password))

    db.commit()

