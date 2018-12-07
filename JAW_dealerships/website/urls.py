from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^home/', views.homePage),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^employee_login/', views.employee_login),
    url(r'^register/', views.register),
]