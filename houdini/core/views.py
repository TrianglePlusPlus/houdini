from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return render(request, 'core/index.html')

def users(request):
	return render(request, 'core/users.html')