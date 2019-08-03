from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import requests
from .models import Joke

DUBLICATE = "Wow its a dublicate ლ(ಠ益ಠლ): "


@login_required(login_url='/login')
def generate_joke(request):
    r = requests.get('https://geek-jokes.sameerkumar.website/api').text
    if Joke.objects.filter(joke=r).count():
        return HttpResponse(DUBLICATE + r)
    joke = Joke(joke=r)
    joke.save()
    return HttpResponse(r)


@login_required(login_url='/login')
@csrf_exempt
def get_joke(request):
    id = request.POST['id']

    joke = Joke.objects.get(id=id)
    return HttpResponse(joke)


@login_required(login_url='/login')
def get_jokes_list(request):
    resp = Joke.objects.all()
    return HttpResponse(resp)


@login_required(login_url='/login')
@csrf_exempt
def update_joke(request):
    id = request.POST['id']
    new_joke = request.POST['joke']
    old_joke = Joke.objects.filter(id=id)
    o_j = old_joke[0]
    old_joke.update(joke=new_joke)
    return HttpResponse(f'Old joke: {o_j}\nNew joke: {new_joke}')


@login_required(login_url='/login')
@csrf_exempt
def remove_joke(request):
    id = request.POST['id']
    if Joke.objects.get(id=id):
        joke = Joke.objects.get(id=id)
        joke.delete()
    return HttpResponse(joke)


@csrf_exempt
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(f"Hello, {username}")
    else:
        return HttpResponse('Wrong user/password')


@csrf_exempt
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("Logged out")
