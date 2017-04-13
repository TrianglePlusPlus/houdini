from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .decorators import *
from datetime import datetime
import requests
import jwt
from core.endpoints import Endpoint

def login(request):
    if request.method == "POST":
        # make a JWT jwt_string of data signed with app_secret
        jwt_string = jwt.encode({
            "email": request.POST.get("email"),
            "password": request.POST.get("password")
        }, settings.HOUDINI_SECRET)

        # POST it to the login endpoint
        r = requests.post(settings.HOUDINI_SERVER + "/endpoints/login", data={
            "app_key": settings.HOUDINI_KEY,
            "jwt_string": jwt_string
        })

        data = Endpoint.authenticate_jwt(r.text, settings.HOUDINI_SECRET)
        if data:
            print(data)
        # TODO: else, u fukt up
        # TODO: handle status code

        # if logged in =>
        if r.status_code == 200:
            # assign r.roles and r.permissions to session variables
            request.session["roles"] = data["roles"]
            request.session["permissions"] = data["permissions"]
            # at login page, save session variables of loggedin_since, & roles+permissions as a set
            request.session["logged_in_since"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            # then redirect to the "next" page (which will hit @login_required again)
            return redirect(request.GET.get("next", ""))
        else:
            # TODO: use messages to be more specific
            response = redirect("login")
            response['Location'] += '?' + urllib.parse.urlencode({'next': request.GET.get("next", "")})
            return response
    else:
        return render(request, "client/login.html")

@login_required
def login_test(request):
    return HttpResponse("logged in successfully!")

@role_required('my new role')
def role_test(request):
    return HttpResponse("logged in successfully, with a role!")

@permission_required('my new permission')
def permission_test(request):
    return HttpResponse("logged in successfully, with a permission!")
