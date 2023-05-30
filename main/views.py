from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,UserCreationForm,AuthForm,PostForm,NewPassForm,EditNoteForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Post
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import ValidationError
# Create your views here.
#login_required(login_url="/login")#if not logged in redirect hapa
def home(request):
    posts=Post.objects.all()
    return render(request,"main/home.html",{
        'posts':posts
    })

def signup_user(request):
    if request.method == "POST":
        form =RegisterForm(request.POST)
        
        if len(form.data.get('password1'))>0:
                if  len(form.data.get('password1'))<=7:
                    messages.error(request,"password is too short")
        elif form.data.get('password1') != form.data.get('password2'):
            messages.error(request, "passwords do not match")
            form=RegisterForm()
        else:
            if form.is_valid():
                user=form.save()
                messages.success(request,"account created,login to complete")
                login(request, user)    
                return redirect("main:home")
            
            
            messages.error(request,"invalid hence user not created")
            form=RegisterForm()
    form=RegisterForm()
    return render(request,"main/signup.html",{
        'form':form
    })

def login_user(request):
    if request.method == "POST":
        form =AuthForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request, "logged in successfully")#message first then redirect
                return redirect("main:home")
            messages.error(request, "user with such credentials doesn't exist")
        messages.error(request,"invalid details")
        form=AuthForm()
    form=AuthForm()
    return render(request,"main/login.html",{
        'form':form
    })


def logout_user(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect("main:login")

@login_required(login_url="/login")#if not logged in redirect hapa
def create_post(request):
    if request.method == "POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)#tusisave kwanza hadi tuadd mwenye ameicreate
            post.created_by=request.user
            post.save()
            messages.success(request, "note added successfully")
            return redirect ("main:home")
    else:
        form=PostForm()
    return render(request, "main/post.html",{
        'form':form
    })

@login_required
def password_change(request):
    user = request.user
    if request.method == "POST":
        form = NewPassForm(user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"password changed successfully")
            return redirect("main:login")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form=NewPassForm(user)
    return render(request, 'main/newp.html', {'form': form})

def note_detail(request,pk):
    note=get_object_or_404(Post,pk=pk)
    return render(request, 'main/detail.html',{'note':note})

def search_view(request):
    query=request.GET.get('query','')
    if query:
        notes=Post.objects.filter(Q(note__contains=query)|Q(title__icontains=query))
    else:
        posts=Post.objects.all().order_by("created_at")
    return render(request, "main/search.html",{
        'query':query,
        'notes':notes
    })
def edit_note(request,pk):
        form=EditNoteForm()
        note=get_object_or_404(Post,pk=pk,created_by=request.user)
        if request.method == "POST":
            form =EditNoteForm(request.POST,instance=note)
            if form.is_valid():
                form.save()
                return redirect("main:detail",pk=note.id)
        else:
            form=EditNoteForm(instance=note)
        return render(request, "main/edit.html",{'form':form})

def delete_note(request,pk):
    post=get_object_or_404(Post,pk=pk,created_by=request.user)
    post.delete()
    return redirect("main:home")