import json

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator

from houdini_server.models import Application, User, Role, Permission
from houdini_client.decorators import login_required, role_required, permission_required
from .forms import ApplicationForm, UserForm, RoleForm, PermissionForm
from .tables import ApplicationTable, UserTable, RoleTable, PermissionTable


def index(request):
    return render(request, 'houdini_admin/index.html')


@login_required
def user_profile(request):
    user = User.objects.get(email=request.user.email)
    return render(request, 'houdini_admin/user_profile.html', {'user': user})


@permission_required("houdini admin")
def hierarchy(request):
    return render(request, 'houdini_admin/hierarchy.html')


@permission_required("houdini admin")
def applications(request):
    table = ApplicationTable(Application.objects.order_by('name').all())
    table.paginate(page=request.GET.get('page', 1), per_page=12)
    return render(request, 'houdini_admin/table.html', {
        'name': 'application',
        'create_button': True,
        'delete_button': True,
        'table': table
    })


@permission_required("houdini admin")
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/applications')
    else:
        form = ApplicationForm()
    return render(request, 'houdini_admin/create.html', {
        'name': 'application',
        'form': form
    })


@method_decorator(permission_required("houdini admin"), name='dispatch')
class ApplicationUpdate(UpdateView):
    """
    Generates the edit form and autofills existing details.
    """
    model = Application
    form_class = ApplicationForm
    template_name = 'houdini_admin/create.html'
    success_url = '/applications'

    def get_context_data(self, *args, **kwargs):
        """
        We have to override this method in order to add `name` to the context
        :param args:
        :param kwargs:
        :return: Supplemented request context
        """
        context = super().get_context_data()
        context['name'] = 'application'
        return context


@permission_required("houdini admin")
def delete_application(request, pk):
    application_to_delete = Application.objects.get(pk=pk)
    message = 'Application "' + application_to_delete.name + '" successfully deleted.'
    if application_to_delete.delete():
        messages.success(request, message)
    return redirect('applications')


@permission_required("houdini admin")
def users(request):
    table = UserTable(User.objects.order_by('date_joined').all())
    table.paginate(page=request.GET.get('page', 1), per_page=12)
    return render(request, 'houdini_admin/table.html', {
        'name': 'user',
        'create_button': False,
        'delete_button': False,
        'table': table
    })


@method_decorator(permission_required("houdini admin"), name='dispatch')
class UserUpdate(UpdateView):
    """
    Generates the edit form and autofills existing details.
    """
    model = User
    form_class = UserForm
    template_name = 'houdini_admin/create.html'
    success_url = '/users'

    def get_context_data(self, *args, **kwargs):
        """
        We have to override this method in order to add `name` to the context
        :param args:
        :param kwargs:
        :return: Supplemented request context
        """
        context = super().get_context_data()
        context['name'] = 'user'
        return context


@permission_required("houdini admin")
def roles(request):
    table = RoleTable(Role.objects.order_by('name').all())
    table.paginate(page=request.GET.get('page', 1), per_page=12)
    return render(request, 'houdini_admin/table.html', {
        'name': 'role',
        'create_button': True,
        'delete_button': True,
        'table': table
    })


@permission_required("houdini admin")
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/roles')
    else:
        form = RoleForm()
    return render(request, 'houdini_admin/create.html', {
        'name': 'role',
        'form': form
    })


@method_decorator(permission_required("houdini admin"), name='dispatch')
class RoleUpdate(UpdateView):
    """
    Generates the edit form and autofills existing details.
    """
    model = Role
    form_class = RoleForm
    template_name = 'houdini_admin/create.html'
    success_url = '/roles'

    def get_context_data(self, *args, **kwargs):
        """
        We have to override this method in order to add `name` to the context
        :param args:
        :param kwargs:
        :return: Supplemented request context
        """
        context = super().get_context_data()
        context['name'] = 'role'
        return context


@permission_required("houdini admin")
def delete_role(request, pk):
    role_to_delete = Role.objects.get(pk=pk)
    message = 'Role "' + role_to_delete.name + '" successfully deleted.'
    if role_to_delete.delete():
        messages.success(request, message)
    return redirect('roles')


@permission_required("houdini admin")
def permissions(request):
    table = PermissionTable(Permission.objects.order_by('name').all())
    table.paginate(page=request.GET.get('page', 1), per_page=12)
    return render(request, 'houdini_admin/table.html', {
        'name': 'permission',
        'create_button': True,
        'delete_button': True,
        'table': table
    })


@permission_required("houdini admin")
def create_permission(request):
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/permissions')
    else:
        form = PermissionForm()
    return render(request, 'houdini_admin/create.html', {
        'name': 'permission',
        'form': form
    })


@method_decorator(permission_required("houdini admin"), name='dispatch')
class PermissionUpdate(UpdateView):
    """
    Generates the edit form and autofills existing details.
    """
    model = Permission
    form_class = PermissionForm
    template_name = 'houdini_admin/create.html'
    success_url = '/permissions'

    def get_context_data(self, *args, **kwargs):
        """
        We have to override this method in order to add `name` to the context
        :param args:
        :param kwargs:
        :return: Supplemented request context
        """
        context = super().get_context_data()
        context['name'] = 'permission'
        return context


@permission_required("houdini admin")
def delete_permission(request, pk):
    permission_to_delete = Permission.objects.get(pk=pk)
    message = 'Permission "' + permission_to_delete.name + '" successfully deleted.'
    if permission_to_delete.delete():
        messages.success(request, message)
    return redirect('permissions')
