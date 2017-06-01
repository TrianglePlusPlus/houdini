from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils import timezone

from datetime import datetime
import jwt
import requests
import urllib.parse

from .decorators import login_required
from .forms import LoginForm, RegisterForm, PasswordChangeForm, PasswordResetForm, PasswordSetForm
from .auth_backend import authenticate_jwt, FailureType

User = get_user_model()


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            r = {}
            user = authenticate(email=email, password=password, response=r)
            # if we were successfully logged in
            if user:
                messages.success(request, "Successfully logged in")

                auth_login(request, user)

                if r.get('http_response') is not None:
                    # decode the JWT received in the HTTP response which contains roles/permissions
                    data = authenticate_jwt(r['http_response'].text, settings.HOUDINI_SECRET)

                    # save the roles and permissions in the session
                    request.session["roles"] = data.get("roles")
                    request.session["permissions"] = data.get("permissions")
                    request.session["logged_in_since"] = timezone.now().strftime(settings.ISO_8601)
                    # then redirect to the "next" page (which will hit @login_required again)
                    return redirect(request.GET.get("next", "index"))
            # otherwise, response will have been filled in with what went wrong
            else:
                if r.get('failure_type') == FailureType.local_failure:
                    # the user exists on the server, but not locally
                    # so => create a local user that will be connected to the existing server user

                    if r.get('http_response') is not None:
                        # decode the JWT received in the HTTP response which contains roles/permissions
                        data = authenticate_jwt(r['http_response'].text, settings.HOUDINI_SECRET)

                        user = User.objects.create_user(
                            email,
                            first_name=data.get("first_name"),
                            last_name=data.get("last_name")
                        )
                        user.save()

                        # TODO: should i auth_login the user here to make it smoother? This exact scenario is
                        #       basically the whole reason we created houdini
                        messages.info(request, "Local user successfully created. Try logging in again.")
                elif r.get('failure_type') == FailureType.server_failure:
                    if r.get('http_response') is not None:
                        messages.error(request, r['http_response'].text)
                    else:
                        messages.error(request, "Authentication Server Error")

                    response = redirect("login")
                    response['Location'] += '?' + urllib.parse.urlencode({'next': request.GET.get("next", "index")})
                    return response
                else:
                    messages.error(request, "Invalid login.")
    else:
        form = LoginForm()

    return render(request, "houdini_client/form.html", {
        'title': 'Login',
        'action': 'Login',
        'form': form}
    )


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

            # POST it to the create_user endpoint
            r = requests.post(
                settings.HOUDINI_SERVER + "/endpoints/create_user",
                # TODO: cert and verify will change in production
                # cert isn't necessary since we have verify=False, but we will leave it
                # as a placeholder for when we are in production with Let's Encrypt
                cert=settings.SSL_DEV_CERT_KEY,
                verify=False,
                # TODO: ^only in development!!!
                data={
                    "app_key": settings.HOUDINI_KEY,
                    "jwt_string": jwt_string
            })

            # if user was successfully created
            if r.status_code == 201:
                # create a local user
                user = User.objects.create_user(
                    form.cleaned_data.get("email"),
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name")
                )
                user.save()

                messages.success(request, "User successfully created! Check your email for an activation link.")
                return redirect("index")
            else:
                messages.error(request, r.text)
    else:
        form = RegisterForm()

    return render(request, "houdini_client/form.html", {
        'title': 'Register',
        'action': 'Register',
        'form': form}
    )


def activate(request, key):
    expired = False
    if request.method == "POST":
        # make a JWT jwt_string of the key signed with app_secret
        jwt_string = jwt.encode({
            "activation_key": request.POST.get('key')
        }, settings.HOUDINI_SECRET)

        # POST it to the regenerate_activation_key endpoint
        r = requests.post(
            settings.HOUDINI_SERVER + "/endpoints/regenerate_activation_key",
            # TODO: cert and verify will change in production
            # cert isn't necessary since we have verify=False, but we will leave it
            # as a placeholder for when we are in production with Let's Encrypt
            cert=settings.SSL_DEV_CERT_KEY,
            verify=False,
            # TODO: ^only in development!!!
            data={
                "app_key": settings.HOUDINI_KEY,
                "jwt_string": jwt_string
        })

        if r.status_code == 200:
            messages.success(request, r.text)
        else:
            messages.error(request, r.text)
    else:
        # make a JWT jwt_string of the key signed with app_secret
        jwt_string = jwt.encode({
            "activation_key": key
        }, settings.HOUDINI_SECRET)

        # POST it to the activate_user endpoint
        r = requests.post(
            settings.HOUDINI_SERVER + "/endpoints/activate_user",
            # TODO: cert and verify will change in production
            # cert isn't necessary since we have verify=False, but we will leave it
            # as a placeholder for when we are in production with Let's Encrypt
            cert=settings.SSL_DEV_CERT_KEY,
            verify=False,
            # TODO: ^only in development!!!
            data={
                "app_key": settings.HOUDINI_KEY,
                "jwt_string": jwt_string
        })

        if r.status_code == 200:
            messages.success(request, r.text)
        elif r.status_code == 403:
            expired = True
            messages.error(request, r.text)
        else:
            messages.error(request, r.text)

    return render(request, "houdini_client/activation.html", {
        'expired': expired,
        'key': key}
    )


def logout(request):
    messages.success(request, "Successfully logged out")

    auth_logout(request)

    request.session["roles"] = []
    request.session["permissions"] = []
    request.session["logged_in_since"] = (timezone.now() - settings.TIME_TO_LIVE).strftime(settings.ISO_8601)
    # then redirect to the home page
    return redirect('index')


@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            # make a JWT jwt_string of data signed with app_secret
            jwt_string = jwt.encode({
                "email": request.user.email,
                "password": form.cleaned_data.get("password"),
                "new_password": form.cleaned_data.get("new_password"),
            }, settings.HOUDINI_SECRET)

            # POST it to the password_change endpoint
            r = requests.post(
                settings.HOUDINI_SERVER + "/endpoints/password_change",
                # TODO: cert and verify will change in production
                # cert isn't necessary since we have verify=False, but we will leave it
                # as a placeholder for when we are in production with Let's Encrypt
                cert=settings.SSL_DEV_CERT_KEY,
                verify=False,
                # TODO: ^only in development!!!
                data={
                    "app_key": settings.HOUDINI_KEY,
                    "jwt_string": jwt_string
            })

            # if user was successfully created
            if r.status_code == 200:
                # Updating the password logs out all other sessions for the user
                # except the current one.
                update_session_auth_hash(request, request.user)
                messages.success(request, r.text)
            else:
                messages.error(request, r.text)
    else:
        form = PasswordChangeForm()

    return render(request, "houdini_client/form.html", {
        'title': 'Change Password',
        'action': 'Change Password',
        'form': form}
    )


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # make a JWT jwt_string of the key signed with app_secret
            jwt_string = jwt.encode({
                "email": request.POST.get('email'),
            }, settings.HOUDINI_SECRET)

            # POST it to the password_reset endpoint
            r = requests.post(
                settings.HOUDINI_SERVER + "/endpoints/password_reset",
                # TODO: cert and verify will change in production
                # cert isn't necessary since we have verify=False, but we will leave it
                # as a placeholder for when we are in production with Let's Encrypt
                cert=settings.SSL_DEV_CERT_KEY,
                verify=False,
                # TODO: ^only in development!!!
                data={
                    "app_key": settings.HOUDINI_KEY,
                    "jwt_string": jwt_string
            })

            if r.status_code == 200:
                messages.success(request, r.text)
            else:
                messages.error(request, r.text)

            form = PasswordResetForm()
    else:
        form = PasswordResetForm()

    return render(request, "houdini_client/form.html", {
        'title': 'Reset Password',
        'action': 'Reset Password',
        'form': form
    })


# very similar to password_change
def password_set(request, key):
    if request.method == "POST":
        form = PasswordSetForm(request.POST)
        if form.is_valid():
            # make a JWT jwt_string of the key signed with app_secret
            jwt_string = jwt.encode({
                "password_reset_key": key,
                "new_password": request.POST.get('new_password')
            }, settings.HOUDINI_SECRET)

            # POST it to the password_set endpoint
            r = requests.post(
                settings.HOUDINI_SERVER + "/endpoints/password_set",
                # TODO: cert and verify will change in production
                # cert isn't necessary since we have verify=False, but we will leave it
                # as a placeholder for when we are in production with Let's Encrypt
                cert=settings.SSL_DEV_CERT_KEY,
                verify=False,
                # TODO: ^only in development!!!
                data={
                    "app_key": settings.HOUDINI_KEY,
                    "jwt_string": jwt_string
            })

            if r.status_code == 200:
                messages.success(request, r.text)
            else:
                messages.error(request, r.text)
    else:
        form = PasswordSetForm()

    return render(request, "houdini_client/form.html", {
        'title': 'Choose a new password',
        'action': 'Set Password',
        'key': key,
        'form': form}
    )


def unauthorized_401(request):
    return render(request, "houdini_client/401.html")
