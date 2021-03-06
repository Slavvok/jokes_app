from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.response import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
import requests
from .models import Joke
from .utils import logging

DUBLICATE = "Wow its a dublicate ლ(ಠ益ಠლ): "


def generate_joke(request):
    if request.user.is_authenticated:
        r = requests.get('https://geek-jokes.sameerkumar.website/api').text
        logging(request)
        if Joke.objects.filter(joke=r, added_by=request.user).count():
            return HttpResponse(DUBLICATE + r)
        joke = Joke(joke=r)
        joke.save(request.user)
        return HttpResponse(r)
    else:
        raise PermissionDenied


@csrf_exempt
def get_joke(request, pk):
    if request.user.is_authenticated:
        # id = request.POST['id']
        logging(request)
        joke = Joke.objects.filter(id=pk, added_by=request.user)
        if joke:
            return HttpResponse(joke)
        else:
            raise Http404("No such joke")
    else:
        raise PermissionDenied


@login_required
def get_jokes_list(request):
    if request.user.is_authenticated:
        logging(request)
        resp = Joke.objects.filter(added_by=request.user)
        return HttpResponse(resp)
    else:
        raise PermissionDenied


@csrf_exempt
def update_joke(request, pk):
    if request.user.is_authenticated:
        logging(request)
        # id = request.POST['id']
        new_joke = request.POST['joke']
        old_joke = Joke.objects.filter(id=pk, added_by=request.user)
        if old_joke:
            o_j = old_joke[0]
            old_joke.update(joke=new_joke)
            return HttpResponse(f'Old joke: {o_j}\nNew joke: {new_joke}')
        else:
            raise Http404("No such joke")
    else:
        raise PermissionDenied


@csrf_exempt
def remove_joke(request, pk):
    if request.user.is_authenticated:
        logging(request)
        # id = request.POST['id']
        joke = Joke.objects.filter(id=pk, added_by=request.user)
        joke_resp = joke[0]
        if joke:
            joke.delete()
        else:
            raise Http404("No such joke")
        return HttpResponse(f"Removed joke: {joke_resp}")
    else:
        raise PermissionDenied


@csrf_exempt
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        pk = get_user_model().id
        logging(req=request, user_id=pk)
        return HttpResponse(f"Hello, {username}")
    else:
        raise HttpResponse("Wrong user/password")


@csrf_exempt
def user_logout(request):
    logging(request)
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("Logged out")


@csrf_exempt
def user_registration(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email)
    if user:
        return HttpResponse(f"User {username} created")