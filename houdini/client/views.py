from django.shortcuts import render, redirect
from django.http import HttpResponse
from .decorators import *
from datetime import datetime
import requests

def login(request):
    if request.method == "POST":
        # TODO: login
        # data = { email, password }
        # make a JWT jwt_string of data signed with app_secret
        # r = requests.post(endpoint, data={'app_key': app_key, jwt_string': jwt_string})

        # assign r.roles and r.permissions to session variables
        # if logged in =>

        # at login page, save session variables of loggedin_since, & roles+permissions as a set
        request.session['logged_in_since'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        # then redirect to the "next" page (which will hit @login_required again)
        return redirect(request.GET.get('next', ""))
    else:
        return render(request, "client/login.html")

@login_required
def login_test(request):
    return HttpResponse("logged in successfully!")
