from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .dbhandler import *


# Create your views here.
def index(request, flag=0):

    if flag == 2:
        reload_db()

    if flag > 1:
        flag = 0

    return render(request, "index.html", {"login_failed": flag})


def homepage(request):
    username = request.GET.get('username', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')
    gender = request.GET.get('gender', '')
    sw = False
    query = "SELECT username, first_name, last_name, gender FROM user_details"

    if username != "" or first_name != "" or last_name != "" or gender != "":
        query += " WHERE "

    if username != "":
        sw = True
        query += " username='" + username + "' "

    if first_name != "":
        if sw:
            query += " OR "
        sw = True
        query += " first_name='" + first_name + "' "

    if last_name != "":
        if sw:
            query += " OR "
        sw = True
        query += " last_name='" + last_name + "' "

    if gender != "":
        if sw:
            query += " OR "
        query += " gender='" + gender + "' "

    data = execute_db(query, [])
    return render(request, "home.html", {"data": data})


def my_login(request):
    username = request.POST.get('username', "")
    passw = request.POST.get('password', "")
    protection_type = request.POST.get('form_type', "")

    if protection_type == "manual_escaping":
        url = reverse(index, kwargs={'flag': 1})
        result = execute_db("SELECT COUNT(*) FROM users WHERE username='" + username + "'"
                            " AND password='" + passw + "'", [])[0][0]
        if result:
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponseRedirect(url)
    elif protection_type == "package-level_escaping":
        url = reverse(index, kwargs={'flag': 1})
        result = execute_db("SELECT COUNT(*) FROM users WHERE username=%s AND password=%s", [username, passw])[0][0]
        if result:
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponseRedirect(url)
    else:
        url = reverse(index, kwargs={'flag': 1})
        return HttpResponseRedirect(url)
