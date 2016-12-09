import json

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import PermissionForm
from .models import Permission, Role
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
    return render(request, 'core/applications.html')


def hierarchy(request):
    return render(request, 'core/hierarchy.html')


def users(request):
    return render(request, 'core/users.html')


def profiles(request):
    return render(request, 'core/profiles.html')


def roles(request):
    return render(request, 'core/roles.html')


def permissions(request):
    permissions = Permission.objects.all()
    return render(request, 'core/permissions.html', {
        'permissions': permissions
    })

def create_permission(request):
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/permissions')
    else:
        form = PermissionForm()
    return render(request, 'core/create.html', {
        'form': form
        })
