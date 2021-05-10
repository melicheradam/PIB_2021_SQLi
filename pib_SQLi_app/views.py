from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .dbhandler import *
from .models import Product
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request, flag=0):

    if flag == 2:
        #reload_db()
        print("db_reload disabled!")
    if flag > 1:
        flag = 0

    return render(request, "index.html", {"login_failed": flag})


def products(request, product_id):
    query = "SELECT COUNT(*) FROM public.products WHERE id=" + str(product_id)
    result = execute_db(query, [])[0][0]
    if result:
        return HttpResponse(product_id)
    else:
        return HttpResponse("<h1>404 Stránka nebola nájdená</h1>", status=404)


def products_orm(request, product_id):
    result = Product.objects.get(pk=product_id)
    if result:
        return HttpResponse(product_id)
    else:
        return HttpResponse("<h1>404 Stránka nebola nájdená</h1>", status=404)


def products_prepared(request, product_id):
    query = "SELECT COUNT(*) FROM public.products WHERE id=%s"
    result = execute_db(query, [product_id])[0][0]
    if result:
        return HttpResponse(product_id)
    else:
        return HttpResponse("<h1>404 Stránka nebola nájdená</h1>", status=404)


def products_selector(request, product_id):
    query = "SELECT COUNT(*) FROM public.products WHERE id=" + str(product_id)
    result = execute_db_selector(query, [])[0][0]
    if result:
        return HttpResponse(product_id)
    else:
        return HttpResponse("<h1>404 Stránka nebola nájdená</h1>", status=404)


def homepage(request):
    protection = request.GET.get('protection', "")

    data = []
    if protection == "" or protection == "no_protection":
        data = homepage_unprotected(request)
    if protection == "prepared_all":
        data = homepage_prepared_all(request)
    if protection == "prepared_some":
        data = homepage_prepared_some(request)

    return render(request, "home.html", {"data": data})


@csrf_exempt
def my_login(request):
    username = request.POST.get('username', "")
    passw = request.POST.get('password', "")
    protection_type = request.POST.get('protection', "")

    if protection_type == "no_protection":
        url = reverse(index, kwargs={'flag': 1})
        result = execute_db("SELECT COUNT(*) FROM users WHERE username='" + username + "'"
                            " AND password='" + passw + "'", [])[0][0]
        if result:
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponseRedirect(url)
    elif protection_type == "prepared":
        url = reverse(index, kwargs={'flag': 1})
        result = execute_db("SELECT COUNT(*) FROM users WHERE username=%s AND password=%s", [username, passw])[0][0]
        if result:
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponseRedirect(url)
    elif protection_type == "manual":
        url = reverse(index, kwargs={'flag': 1})
        result = execute_db("SELECT COUNT(*) FROM users WHERE username='" + username.replace("'", "").replace(";", "").replace("-", "") + "'"
                            " AND password='" + passw.replace("'", "").replace(";", "").replace("-", "") + "'", [])[0][0]
        if result:
            return HttpResponseRedirect("/home/")
        else:
            return HttpResponseRedirect(url)
    else:
        url = reverse(index, kwargs={'flag': 1})
        return HttpResponseRedirect(url)
