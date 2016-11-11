from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')


def applications(request):
    return render(request, 'core/base.html')


def directories(request):
    return render(request, 'core/directories.html')


def users(request):
    return render(request, 'core/users.html')


def roles(request):
    return render(request, 'core/base.html')


def permissions(request):
    return render(request, 'core/base.html')
