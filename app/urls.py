from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/',views.admin_login, name='admin_login'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('contact/', views.contact, name='contact'),
    path('view_messages/', views.view_messages, name='view_messages'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('messages/reply/<int:message_id>/', views.reply_messages, name='reply_messages'),
    path('messages/mark_viewed/<int:message_id>/', views.mark_viewed, name='mark_viewed'),
]