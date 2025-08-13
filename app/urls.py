from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/',views.admin_login, name='admin_login'),
    path('contact/', views.contact, name='contact'),
    path('view_messages/', views.view_messages, name='view_messages'),
    path('message/<int:message_id>/', views.view_message_detail, name='view_message_detail'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
]