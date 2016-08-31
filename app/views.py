__author__ = 'noris7012'

from django.shortcuts import render_to_response, redirect

def index(request):
    return render_to_response('index.html')