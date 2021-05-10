"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pib_SQLi_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:flag>', views.index, name='index'),
    path('', views.index, name='index'),
    path('login/', views.my_login, name="my_login"),
    path('home/', views.homepage, name="homepage"),
    path('products/unprotected/<product_id>', views.products, name="products"),
    path('products/prepared/<product_id>', views.products_prepared, name="products"),
    path('products/selector/<product_id>', views.products_selector, name="products"),
    path('products/orm/<product_id>', views.products_orm, name="products"),
]
