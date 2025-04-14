from django.shortcuts import render,redirect
from django.views import generic
from .models import Post
from rest_framework import viewsets
from .serializer import PostSerializer
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 注册后自动登录
            messages.success(request,'Register success!!')
            return redirect("home")  # 重定向到主页（确保有 'home' 的 URL）
    else:
        form = NewUserForm()  # GET 请求时初始化空表单
    return render(request, "register.html", {"register_form": form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    form = AuthenticationForm()
    return render(request,'login.html',{'login_form':form})

def logout_request(request):
    logout(request)
    messages.info(request,'You have successfully logged out')
    return redirect('home')
