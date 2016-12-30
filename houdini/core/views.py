import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from django.contrib import messages

from .forms import PermissionForm, RoleForm
from .models import Permission, Role
from .tables import PermissionTable, RoleTable
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
    table = RoleTable(Role.objects.order_by('name').all())
    table.paginate(page=request.GET.get('page', 1), per_page=2)
    return render(request, 'core/table.html', {
        'name': 'role',
        'table': table
    })


def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/roles')
    else:
        form = RoleForm()
    return render(request, 'core/create.html', {
        'name': 'role',
        'form': form
    })

class RoleUpdate(UpdateView):
    """
    Generates the edit form and autofills existing details.
    """
    model = Role
    form_class = RoleForm
    template_name = 'core/create.html'
    success_url = '/roles'

    def get_context_data(self, *args, **kwargs):
        """
        We have to override this method in order to add `name` to the context
        :param args:
        :param kwargs:
        :return: Supplemented request context
        """
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'role'
        return context


def delete_role(request, role_id):
    role_to_delete = Role.objects.get(pk=role_id)
    message = 'Role "' + role_to_delete.name + '" successfully deleted.'
    if role_to_delete.delete():
        messages.success(request, message)
    return redirect('roles')


def permissions(request):
    table = PermissionTable(Permission.objects.order_by('name').all())
    table.paginate(page=request.GET.get('page', 1), per_page=2)
    return render(request, 'core/table.html', {
        'name': 'permission',
        'table': table
    })
    # permission_list = Permission.objects.order_by('name').all()
    # paginator = Paginator(permission_list, 25)

    # page = request.GET.get('page')
    # try:
    #     permissions = paginator.page(page)
    # except PageNotAnInteger:
    #     permissions = paginator.page(1)
    # except EmptyPage:
    #     permissions = paginator.page(paginator.num_pages)

    # return render(request, 'core/permissions.html', {
    #     'permissions': permissions
    # })


def create_permission(request):
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/permissions')
    else:
        form = PermissionForm()
    return render(request, 'core/create.html', {
        'name': 'permission',
        'form': form
    })


class PermissionUpdate(UpdateView):
    """
    Generates the edit form and autofills existing details.
    """
    model = Permission
    form_class = PermissionForm
    template_name = 'core/create.html'
    success_url = '/permissions'

    def get_context_data(self, *args, **kwargs):
        """
        We have to override this method in order to add `name` to the context
        :param args:
        :param kwargs:
        :return: Supplemented request context
        """
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'permission'
        return context


def delete_permission(request, permission_id):
    permission_to_delete = Permission.objects.get(pk=permission_id)
    message = 'Permission "' + permission_to_delete.name + '" successfully deleted.'
    if permission_to_delete.delete():
        messages.success(request, message)
    return redirect('permissions')
