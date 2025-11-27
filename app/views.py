from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, get_user_model
from .models import Message
from django.http import HttpResponse
from .forms import ReplyForm
from django.conf import settings

def is_superuser(user):
    return user.is_superuser


def home(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        if full_name and email and message_text:
            Message.objects.create(
                full_name=full_name,
                email=email,
                message=message_text,
            )
            # If AJAX request, return JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
            else:
                messages.success(request, 'Your message has been sent successfully!')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Please fill in all fields before submitting.'})
            else:
                messages.error(request, 'Please fill in all fields before submitting.')
        
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return redirect('home')  

    return render(request, 'home.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('view_messages')
        else:
            messages.error(request, "Access denied. Only Admins can login.")
            return redirect('admin_login')

    return render(request, 'admin_login.html')


@user_passes_test(is_superuser)
def view_messages(request):
    msg_list = Message.objects.all().order_by('-created_at')
    return render(request, 'view_messages.html', {'contact_list': msg_list})

@user_passes_test(is_superuser)
def reply_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)

    if not msg.is_read:
        msg.is_read = True
        msg.save()

    if request.method == "POST":
        response = request.POST.get('response')
        msg.response = response
        msg.status = "replied"
        msg.save()

        send_mail(
            subject="Reply to your message",
            message=response,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[msg.email],
        )
        messages.success(request, "Reply sent successfully!")
        return redirect("view_messages")
    
    return render(request, "reply_message.html", {'message': msg})

def new_messages_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return {'new_messages_count': Message.objects.filter(status='new').count()}
    return {'new_messages_count': 0}


@user_passes_test(is_superuser)
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)
    msg.delete()
    messages.success(request, 'Message deleted successfully!')
    return redirect('view_messages')

def create_superuser(request):
    User = get_user_model()
    username =  'admin'
    email = 'kelvinkatwai@gmail.com'
    password = 'cekret'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse("Superuser created successfully!")
    return HttpResponse("Superuser already exists!")