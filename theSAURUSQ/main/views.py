from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import Question, Answer, Comment
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

#Homepage
def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        quests=Question.objects.filter(title__icontains=q).order_by('-id')
    else:
        quests=Question.objects.all().order_by('-id')
    paginator=Paginator(quests,1)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request, 'home.html', {'quests':quests})


#Detail

def detail(request,id):
    quest=Question.objects.get(pk=id)
    tags=quest.tags.split(',')
    answer=Answer.objects.get(question=quest)
    comments=Comment.objects.filter(answer=answer).order_by('-id')
    return render(request, 'detail.html', {
        'quest':quest,
        'tags':tags,
        'answer':answer,
        'comments':comments
        })


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            message = 'Usename or password is incorrect'
            form = AuthenticationForm()
            return render(request, 'login.html', {'form': form, 'message': message})
    form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})


@csrf_exempt
def signup(request):
    if request.method == "POST":
        user = User()
        user.username = request.POST.get('username')
        user.is_superuser = True
        user.is_staff = True
        user.password = make_password(request.POST.get('password1'))
        user.save()
        return redirect('/')

    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('/login')