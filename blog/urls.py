"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from blog import views
urlpatterns = [
    path('blog/', views.index_page,name='blog'),
    # path('<page_name>/',to_page,name='page'),
    # path('',index_page),
    path('blog_detail/<article_id>/',views.single_blog,name="single_blog"),
    path('create_comment',views.create_comment,name="create_comment"),
    path('json_test' , views.json_test , name="json_test"),
    path('login/' , views.login_page , name="login"),
    path('category/' , views.to_cateogry , name="catetory"),
    path('contact/' , views.to_contact , name="contact"),
    path('404/' , views.to_error , name="error"),
    path('validate_login' , views.validate_login , name="validate_login"),
    path('session_test' , views.session_test , name="session_test"),
    path('logout' , views.logout , name="logout"),
    path('register' , views.reg_page , name="register"),
    path('validate_regemail' , views.validate_regemail , name="validate_regemail"),
    path('validate_username' , views.validate_username , name="validate_username"),
    path('commit_register' , views.commit_register , name="commit_register"),
]
