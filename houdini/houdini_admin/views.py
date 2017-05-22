from django.shortcuts import render
from houdini_client.decorators import login_required, role_required, permission_required

@login_required
def login_test(request):
    return render(request, "houdini_admin/login_test.html")

@role_required('new role')
def role_test(request):
    return render(request, "houdini_admin/role_test.html")

@permission_required('new permission')
def permission_test(request):
    return render(request, "houdini_admin/permission_test.html")

def unauthorized_401(request):
    return render(request, "houdini_admin/401.html")
