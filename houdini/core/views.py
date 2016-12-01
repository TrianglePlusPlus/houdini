import json

from django.http import HttpResponse
from django.shortcuts import render

from .models import Role
from .utils import JsonResponse


def index(request):
    # dir_it = Role.create('Director of IT')
    # dir_it.add_permission('timelord')
    # dir_it.add_permission('backdoor')
    # dir_it.add_permission('over9000')
    # dir_it.add_parent('it')
    # dir_it.add_parent('director')
    # dir_it.save()
    # ceo = Role.create('CEO')
    # ceo.add_permission('meep')
    # ceo.add_parent('director')
    # ceo.add_parent('officer')
    # ceo.save()
    # return JsonResponse(Role.get_json())
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
