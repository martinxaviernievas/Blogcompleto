from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def helloword(request):
    return render(request,'signup.html',{
       'forms': UserCreationForm
    })