from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tools/', views.tool_list, name='tool_list'),
    path('tools/<slug:slug>/', views.tool_detail, name='tool_detail'),
]
