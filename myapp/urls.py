from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.input, name='input'),
    path('submit', views.response, name='response'),
]