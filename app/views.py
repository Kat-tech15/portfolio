from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import ContactMessage
from .forms import ContactForm, ReplyForm

# Create your views here.

def home(request):
    return render(request, 'base.html')

def about(request):
    context = {}
    return render(request, 'about.html', context)

def skills(request):
    return render(request, 'skills.html')

def contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            message=message,
        )

        contact.save()
        messages.success(request, 'Your message has been sent successfully!')   
        return redirect('contact')

    return render(request, 'contact.html')

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def view_messages(request):
    messages = ContactMessage.objects.all().order_by('-id')
    return render(request, 'view_messages.html', {'messages': messages})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and  user.is_superuser:
            login(request, user)
            return render(request,'view_messages.html',{'messages': ContactMessage.objects.all().order_by('-id')})
        else:
            messages.error(request, "Access denied. Only Admins can login.")
            return redirect(request, 'admin-login')
        
    return render(request, 'admin_login.html')

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    messages.success(request,'Message deleted successfully!')
    return redirect('view_messages')

@login_required
def mark_viewed(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.viewed = True
    message.save()
    messages.success(request, 'Message marked as viewed!')
    return redirect('view_messages')


@login_required
def reply_messages(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply_text = form.cleaned_data['reply']
            send_mail(
                subject='Reply to your message',
                message=reply_text,
                from_email="kelvinkatwai@gmail.com",
                recipient_list=[message.email],    
            )
            message.replied = True
            message.save()
            messages.success(request, 'Reply sent successfully!')
            return redirect('view_messages')
    else:
        # this runs on GET (and any non-POST), so form is always defined below
        form = ReplyForm()

    return render(request, 'reply_messages.html', {
        'form': form,
        'message': message
    })