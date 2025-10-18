from django.shortcuts import render
from django.utils import translation


# Create your views here.
def index(request):
    user_language = translation.get_language()
    context = {}
    return render(request,"app_Home/index.html",context)