from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .models import Message
from .forms import ReplyForm,MessageForm
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
            messages.success(request, 'Your message has been sent successfully!')
        else:
            messages.error(request, 'Please fill in all fields before submitting.')

        return redirect('home')  # reload home page after form submission

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


@login_required
@user_passes_test(is_superuser)
def view_messages(request):
    messages = Message.objects.all().order_by('-id')
    return render(request, 'view_messages.html', {'messages': messages})


@login_required
@user_passes_test(is_superuser)
def view_message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.status == 'new':
        message.status = 'viewed'
        message.save()

    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=message)
        if form.is_valid():
            message = form.save(commit=False)
            message.status = 'replied'
            message.save()

            send_mail(
                subject=f"Reply to your message",
                message=message.reply,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[message.email],
            )

            messages.success(request, 'Reply sent successfully!')
            return redirect('view_messages')
    else:
        form = ReplyForm(instance=message)

    return render(request, 'view_message_detail.html', {
        'message': message,
        'form': form
    })

@login_required
@user_passes_test(is_superuser)
def view_notification(request):
    messages = Message.objects.filter(status='new').order_by('-created_at')
    messages.update(status='viewed')
    
    return render(request, 'view_messages.html', {'messages': messages})

def new_messages_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return {'new_messages_count': Message.objects.filter(status='new').count()}
    return {'new_messages_count': 0}

@login_required
@user_passes_test(is_superuser)
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    messages.success(request, 'Message deleted successfully!')
    return redirect('view_messages')
