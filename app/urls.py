from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/',views.admin_login, name='admin_login'),
    path('view_messages/', views.view_messages, name='view_messages'),
    path('messages/', views.view_messages, name='view_messages'),
    path('message/reply/<int:message_id>/', views.reply_message, name='reply_message'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('create-superuser/', views.create_superuser),
]