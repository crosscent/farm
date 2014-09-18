# Create your views here.
from django.shortcuts import render

def index(request):
    return render_to_response('web\index.html')