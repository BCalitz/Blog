from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms.models import model_to_dict
from django import forms
# Create your views here.


class SignUpForm(forms.Form):
    fname = forms.CharField(label="First Name",widget=forms.TextInput(attrs={'class': 'block'}))
    sname = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class': 'block'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'block content-form'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block'}), label="Password")
    cpass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block'}), label="Confirm Password")

class SignInForm(forms.Form):
    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={'class': 'block'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block'}), label="Password")

class PostForm(forms.Form):
    title =forms.CharField(label='Title',widget=forms.TextInput(attrs={'class': 'block'}))
    content= forms.CharField(widget=forms.Textarea(attrs={'class': 'block'}))


def index(request):
    if "log" not in request.session:
        request.session["log"] = {
            'loggedin': False,
            'author': None,
        }
    return render(request, "home/index.html", {
        "blogs": Blog.objects.all(),
        'log': request.session['log']
    })


def blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, "home/blog.html", {
        "blog": blog,
        'log': request.session['log']
    })


def author(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, "home/author.html", {
        'author': author,
        'posts': author.posts.all(),
        'log': request.session['log']
    })


def authors(request):
    authors = Author.objects.all()
    return render(request, "home/authors.html", {
        'authors': authors.order_by('author_sname','author_fname'),
        'log': request.session['log']
    })


def login(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = Author.objects.filter(author_email=email)
            if not user:
                return render(request, "home/login.html", {
                    'message': 'Invalid Email',
                    'form': form,
                })
            else:
                user = Author.objects.get(author_email=email)
                if user.author_pass != password:
                    return render(request, "home/login.html", {
                        'message': 'Invalid Credentials',
                        'form': form,
                    })
                else:
                    (request.session['log'])['loggedin'] = True
                    (request.session['log'])['author'] = model_to_dict(user)
                    request.session.modified = True
                    return HttpResponseRedirect(reverse("home"))
    return render(request, "home/login.html",{
        'form': SignInForm,
    })


def logout(request):
    (request.session['log'])['loggedin'] = False
    (request.session['log'])['author'] = None
    request.session.modified = True
    return HttpResponseRedirect(reverse("home"))


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data["fname"]
            sname = form.cleaned_data["sname"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            cpass = form.cleaned_data["cpass"]
            if not Author.objects.filter(author_email=email):
                if password == cpass:
                    user = Author(author_fname=fname, author_sname=sname,
                                author_email=email, author_pass=password)
                    user.save()
                    (request.session['log'])['loggedin'] = True
                    (request.session['log'])['author'] = model_to_dict(user)
                    request.session.modified = True
                    return HttpResponseRedirect(reverse("home"))
                else:
                    return render(request, "home/signup.html",{
                        'form':form,
                        'message': 'Passwords don\'t match!',
                    })
            else:
                return render(request, "home/signup.html",{
                    'form':form,
                    'message': 'Email already exists',
                })
    return render(request, "home/signup.html",{
        'form': SignUpForm
    })

def post(request):
    if request.method == "POST":
        form =PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = Author.objects.get(id =((request.session['log'])['author'])['id'])
            posting = Blog(blog_title = title, blog_context=content, blog_author= author)
            posting.save()
            return HttpResponseRedirect(reverse("home"))
    return render(request, 'home/post.html',{
        'form' : PostForm,
        'log': request.session['log']
    })


