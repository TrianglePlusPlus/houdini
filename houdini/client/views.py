from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils import timezone

# TODO: make sure all datetimes are offset aware?
from datetime import datetime
import jwt
import requests
import urllib.parse

from core.endpoints import Endpoint
from core.models import User
from .decorators import login_required, role_required, permission_required
from .forms import LoginForm, RegisterForm

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

            # TODO: needs to become admin.models.User
            user = User.objects.get(email=request.POST.get("email"))
            if user is None:
                # TODO: in this case, i.e. where you authenticate successfully against the auth server
                #       but not locally, we might want to suggest that the user create a local account
                #       that will link up with the existing auth server account (how would we do this?)
                # TODO: i also think i need to include core.http
                return HttpResponseUnauthorized('Invalid user/password combination')
            auth_login(request, user)

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
                "first_name": form.cleaned_data.get("first_name"),
                "middle_name": form.cleaned_data.get("middle_name"),
                "last_name": form.cleaned_data.get("last_name"),
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
                # TODO: redirect to a "registration successful view"?
                messages.success(request, "User successfully created! Check your email for an activation link.")
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

def activate(request, key):
    expired = False
    if request.method == "POST":
        try:
            user = User.objects.get(activation_key=request.POST.get('key'))
            if user.key_expires < timezone.now():
                if not user.is_active:
                    user.regenerate_activation_key()
                    user.save()
                    expired = False
                    messages.success(request, "Check your email for a new activation link.")
                else:
                    messages.error(request, "User already activated")
            # TODO: else?
        except User.DoesNotExist:
            messages.error(request, "Invalid activation key")
    else:
        try:
            user = User.objects.get(activation_key=key)
            if user.key_expires > timezone.now():
                if not user.is_active:
                    user.is_active=True
                    user.save()
                    messages.success(request, "User successfully activated!")
                else:
                    messages.error(request, "User already activated")
            else:
                if not user.is_active:
                    messages.error(request, "Activation key has expired")
                    # so we can offer to generate them a new activation key
                    expired = True
                else:
                    messages.error(request, "User already activated")

        except User.DoesNotExist:
            messages.error(request, "Invalid activation key")

    return render(request, "client/activation.html", {'expired': expired, 'key': key})

def logout(request):
    # make a JWT jwt_string of data signed with app_secret
    jwt_string = jwt.encode({
        "email": request.POST.get("email"),
    }, settings.HOUDINI_SECRET)

    # POST it to the logout endpoint
    r = requests.post(settings.HOUDINI_SERVER + "/endpoints/logout", data={
        "app_key": settings.HOUDINI_KEY,
        "jwt_string": jwt_string
    })

    # if we were successfully logged out
    if r.status_code == 200:
        messages.success(request, "Successfully logged out")

        auth_logout(request)

        data = Endpoint.authenticate_jwt(r.text, settings.HOUDINI_SECRET)
        # TODO: ?
        request.session["roles"] = []
        request.session["permissions"] = []
        request.session["logged_in_since"] = (datetime.now() - settings.TIME_TO_LIVE).strftime("%Y-%m-%dT%H:%M:%S")
        # then redirect to the home page
        return redirect('index')
    else:
        # TODO: will a logout ever actually fail? do we even need to hit the server?
        # TODO: use messages to be more specific on other status codes
        messages.error(request, r.text)

        return redirect('index')

@login_required
def login_test(request):
    return render(request, "client/login_test.html")

@role_required('new role')
def role_test(request):
    return render(request, "client/role_test.html")

@permission_required('new permission')
def permission_test(request):
    return render(request, "client/permission_test.html")

def unauthorized_401(request):
    return render(request, "client/401.html")
