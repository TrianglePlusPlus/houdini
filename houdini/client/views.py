from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from .decorators import *
from .forms import *
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

        # if we were successfully logged in
        if r.status_code == 200:
            messages.success(request, "Successfully logged in")

            # assign r.roles and r.permissions to session variables
            data = Endpoint.authenticate_jwt(r.text, settings.HOUDINI_SECRET)
            # TODO: check if data == None?
            # TODO: convert roles and permissions to sets?
            request.session["roles"] = data["roles"]
            request.session["permissions"] = data["permissions"]
            # at login page, save session variables of loggedin_since, & roles+permissions as a set
            request.session["logged_in_since"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            # then redirect to the "next" page (which will hit @login_required again)
            return redirect(request.GET.get("next", "index"))
        else:
            # TODO: use messages to be more specific on other status codes
            messages.error(request, r.text)

            response = redirect("login")
            response['Location'] += '?' + urllib.parse.urlencode({'next': request.GET.get("next", "index")})
            return response
    else:
        form = LoginForm()
        return render(request, "client/login.html", {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # make a JWT jwt_string of data signed with app_secret
            jwt_string = jwt.encode({
                "email": form.cleaned_data.get("email"),
                "password": form.cleaned_data.get("password")
            }, settings.HOUDINI_SECRET)

            # POST it to the login endpoint
            r = requests.post(settings.HOUDINI_SERVER + "/endpoints/create_user", data={
                "app_key": settings.HOUDINI_KEY,
                "jwt_string": jwt_string
            })

            # if user was successfully created
            if r.status_code == 201:
                # TODO: check content of response? assign anything to session?
                messages.success(request, "User successfully created")
                return redirect("index")
            else:
                # TODO: use messages to be more specific on other status codes
                messages.error(request, r.text)
                return render(request, "client/register.html", {'form': form})
        else:
            return render(request, "client/register.html", {'form': form})
    else:
        form = RegisterForm()
        return render(request, "client/register.html", {'form': form})

@login_required
def login_test(request):
    return HttpResponse("logged in successfully!")

@role_required('my old role')
def role_test(request):
    return HttpResponse("logged in successfully, with a role!")

@permission_required('my new permission')
def permission_test(request):
    return HttpResponse("logged in successfully, with a permission!")

def unauthorized_401(request):
    return render(request, "client/401.html")
