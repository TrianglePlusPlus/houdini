import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    permission_list = Permission.objects.order_by('name').all()
    paginator = Paginator(permission_list, 25)

    page = request.GET.get('page')
    try:
        permissions = paginator.page(page)
    except PageNotAnInteger:
        permissions = paginator.page(1)
    except EmptyPage:
        permissions = paginator.page(paginator.num_pages)

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

def edit_permission(request, permission_id):
    permission = Permission.objects.get(pk=permission_id)
    if permission:
        
    return redirect('/permissions')

def delete_permission(request, permission_id):
    pass
