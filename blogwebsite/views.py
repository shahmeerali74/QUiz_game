from django.http import HttpResponse
from django.shortcuts import render
import requests
def index(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'aboutus.html')

def game(request):
        
    # api_url="https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=multiple"
    # questions=requests.get(api_url).json().get('results',[])
    return render(request, 'game.html')
# ,{'questions':questions}

