from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from blog.models import Post
from .models import Projects
from .forms import ContactForm


def home(request):
    title_text = 'Home'
    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:2]
    projects = Projects.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:3]
    return render(request, 'home/home.html', {'posts': post_list, 'title': title_text, 'projects': projects})


def about(request):
    title_text = 'About'
    return render(request, 'home/about.html', {'title': title_text})


def projects(request):
    title_text = 'Projects'
    projects = Projects.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'home/projects.html', {'title': title_text, 'projects': projects})


def contact(request):
    title_text = 'Contact'
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            content = form.cleaned_data['content']
            try:
                email = EmailMessage(contact_name,
                                    content,
                                    contact_email,
                                    ['mogerweb@gmail.com'],
                                     reply_to=[contact_email],
                                   )
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('./thanks/')
    return render(request, 'home/contact.html', {'title': title_text, 'form': form})


def thanks(request):
    title_text = 'Thank you!'
    return render(request, 'home/thanks.html', {'title': title_text})
