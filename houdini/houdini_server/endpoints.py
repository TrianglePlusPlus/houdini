from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import json
import jwt

from .models import Application, User, RolesToPermissions
from .http import *
from .auth_backend import authenticate as server_authenticate

# Endpoints

# login
# create user
# activate user
# change password
# reset password
# add role          ?
# remove role       ?
# update user       ?

class Endpoint(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.jwt_string = None
        self.data = None
        self.is_valid_request = True

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def authenticate_jwt(jwt_string, app_secret):
        # Check to see if the signature is correct
        try:
            data = jwt.decode(jwt_string, app_secret)
            return data
        except jwt.DecodeError:
            return None

    @staticmethod
    def get_app(app_key):
        app = Application.objects.filter(key=app_key)
        if app.count() != 1:
            return None
        else:
            return app[0]

    def validate_request(self):
        """
        Checks to make sure that the request is valid:
             - Method is POST
             - App key exists and the corresponding app exists
             - JWT string exists
             - JWT is properly signed
         Sets self.is_valid_request to False if any tests fail
        :return: Error response if applicable, otherwise no return type
        """
        if self.request.method != 'POST':
            self.is_valid_request = False
            return HttpResponseInternalServerError(reason="Request method is not POST.")
        app_key = self.request.POST.get('app_key', None)
        self.app = self.get_app(app_key)
        if self.app is None:
            self.is_valid_request = False
            return HttpResponseInternalServerError(reason="App not found.")
        self.jwt_string = self.request.POST.get('jwt_string', None)
        if self.jwt_string is None:
            # We'll return a server error if they don't actually send anything
            self.is_valid_request = False
            return HttpResponseInternalServerError(reason="JWT string missing.")
        self.data = self.authenticate_jwt(self.jwt_string, self.app.secret)
        if self.data is None:
            self.is_valid_request = False
            return HttpResponseUnauthorized(reason="Web token signature invalid.")
            # App exists and the data is signed correctly


class LoginEndpoint(Endpoint):
    def post(self, request):
        error_response = self.validate_request()
        if not self.is_valid_request:
            return error_response
        email = self.data['email']
        password = self.data['password']
        user = server_authenticate(email=email, password=password)
        if user is None:
            return HttpResponseUnauthorized(reason='Invalid user/password combination')
            # TODO: or user could just be inactive. do we need to be more specific?

        # Get all of the roles for the profiles they are logging in as
        app_roles = set(self.app.roles.all())
        # Get all of the roles the user has
        user_roles = set(user.roles.all())
        relevant_roles = app_roles.intersection(user_roles)
        # Now get all of the permissions for every role
        permissions = set()
        for role in relevant_roles:
            role_permissions = set(json.loads(RolesToPermissions.objects.get(role=role).permissions))
            permissions.update(role_permissions)
        response_data = {}
        response_data['permissions'] = list(permissions)
        response_data['roles'] = [role.name for role in relevant_roles]
        response_data['roles'] += [role.slug for role in relevant_roles]
        response_jwt = jwt.encode(response_data, self.app.secret)
        return HttpResponse(response_jwt)


class CreateUserEndpoint(Endpoint):
    def post(self, request):
        error_response = self.validate_request()
        if not self.is_valid_request:
            return error_response
        first_name = self.data['first_name']
        middle_name = self.data['middle_name']
        last_name = self.data['last_name']
        email = self.data['email']
        password = self.data['password']

        # Check to see whether a user with that username exists
        if User.objects.filter(email=email).count() != 0:
            # A user already exists so return an error
            return HttpResponseConflict('User already exists')
            # TODO: "email already in use?"

        # create user
        user = User.objects.create_user(
            email, password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name
        )
        # TODO: default roles/permissions?
        user.save()

        # TODO: what to send back?
        # response_data = {}
        # response_jwt = jwt.encode(response_data, self.app.secret)
        # return HttpResponse(response_jwt)
        return HttpResponseCreated()


class ActivateUserEndpoint(Endpoint):
    def post(self, request):
        error_response = self.validate_request()
        if not self.is_valid_request:
            return error_response
        key = self.data['activation_key']

        try:
            user = User.objects.get(activation_key=key)
        except User.DoesNotExist:
            # status code 400
            # or 404: User not found?
            return HttpResponseBadRequest("Invalid activation key")

        if user.is_active:
            # status code 200; it's not a failure
            return HttpResponse("User already activated")

        if user.activation_key_expires < timezone.now():
            # status code 403
            return HttpResponseForbidden("Activation key has expired")

        # the activation key was valid, the user is currently inactive, and the key hasn't expired!
        user.is_active=True
        user.save()
        # status code 200
        return HttpResponse("User successfully activated!")


class RegenerateActivationKeyEndpoint(Endpoint):
    def post(self, request):
        error_response = self.validate_request()
        if not self.is_valid_request:
            return error_response
        key = self.data['activation_key']

        try:
            user = User.objects.get(activation_key=key)
        except User.DoesNotExist:
            # status code 400
            # or 404: User not found?
            return HttpResponseBadRequest("Invalid activation key")

        if user.is_active:
            # status code 200; it's not a failure
            return HttpResponse("User already activated")

        # We don't care if the activation key has not expired, we will just regenerate
        # a new one if they mistakenly ask

        # the activation key was valid, the user is currently inactive, and the key has expired!
        user.regenerate_activation_key()
        user.save()
        # status code 200
        return HttpResponse("Check your email for a new activation link.")


class PasswordChangeEndpoint(Endpoint):
    def post(self, request):
        error_response = self.validate_request()
        if not self.is_valid_request:
            return error_response
        email = self.data['email']
        password = self.data['password']
        new_password = self.data['new_password']

        user = server_authenticate(email=email, password=password)
        if user is None:
            # status code 401
            return HttpResponseUnauthorized(reason="Old password was incorrect")

        user.set_password(new_password)
        user.save()
        # status code 200
        return HttpResponse("Password successfully changed")


class PasswordResetEndpoint(Endpoint):
    def post(self, request):
        error_response = self.validate_request()
        if not self.is_valid_request:
            return error_response
        email = self.data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # status code 400
            # or 404: User not found?
            return HttpResponseBadRequest("Invalid email")

        if not user.is_active:
            # status code 401
            return HttpResponseUnauthorized(reason="User is inactive")

        # send an email with a link to reset their password
        user.generate_password_reset_key()
        user.send_password_reset_email()
        user.save()
        # status code 200
        return HttpResponse("Check your email for a link to reset your password.")


class PasswordSetEndpoint(Endpoint):
    def post(self, request):
        error_response = self.validate_request()
        if not self.is_valid_request:
            return error_response
        key = self.data['password_reset_key']
        new_password = self.data['new_password']

        try:
            user = User.objects.get(password_reset_key=key)
        except User.DoesNotExist:
            # status code 400
            # or 404: User not found?
            return HttpResponseBadRequest("Invalid password reset link")

        if not user.is_active:
            # status code 401
            return HttpResponseUnauthorized(reason="User is inactive")

        if user.password_key_expires < timezone.now():
            # status code 403
            return HttpResponseForbidden("Password reset link has expired")

        # the password reset key was valid, the user is currently active, and the key hasn't expired!
        user.set_password(new_password)
        user.save()
        # status code 200
        return HttpResponse("Your password has been changed")
