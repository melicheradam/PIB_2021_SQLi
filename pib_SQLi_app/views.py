from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json


# Create your views here.
def index(request, login_status=0):

    return render(request, "index.html", {"login_failed": login_status})


def homepage(request):
    return render(request, "home.html", None)


def my_login(request):
    username = request.POST.get('username', "")
    passw = request.POST.get('password', "")
    protection_type = request.POST.get('protection_type', "")
    if protection_type == "manual_escaping":
        url = reverse(index, kwargs={'login_status': 1})
        if username == "adam" and passw == "adam":
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponseRedirect(url)
    elif protection_type == "package-level_escaping":
        url = reverse(index, kwargs={'login_status': 2})
        if username == "adam" and passw == "adam":
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponseRedirect(url)
    else:
        url = reverse(index, kwargs={'login_status': 3})
        return HttpResponseRedirect(url)
