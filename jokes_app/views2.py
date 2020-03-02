from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.core.serializers import serialize
import requests
from .models import Joke
from .utils import logging

DUBLICATE = "Wow its a dublicate ლ(ಠ益ಠლ): "


class GenerateJokeView(LoginRequiredMixin, View):
    def get(self, request):
        r = requests.get('https://geek-jokes.sameerkumar.website/api').text
        logging(request)
        if Joke.objects.filter(joke=r, added_by=request.user).count():
            return HttpResponse(DUBLICATE + r)
        joke = Joke(joke=r)
        joke.save(request.user)
        return JsonResponse({'joke': r})


class GetJokeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        logging(request)
        joke = Joke.objects.filter(id=pk, added_by=request.user)
        if joke:
            return HttpResponse(joke)
        else:
            raise Http404("No such joke")


class GetJokesListView(LoginRequiredMixin, View):
    def get(self, request):
        logging(request)
        resp = serialize('json', Joke.objects.filter(added_by=request.user))
        return HttpResponse(resp)


class UpdateJokeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        logging(request)
        # id = request.POST['id']
        new_joke = request.POST['joke']
        old_joke = Joke.objects.filter(id=pk, added_by=request.user)
        if old_joke:
            o_j = old_joke[0]
            old_joke.update(joke=new_joke)
            return HttpResponse(f'o: {o_j}, n: {new_joke}')
        else:
            raise Http404("No such joke")


class RemoveJokeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        logging(request)
        # id = request.POST['id']
        joke = Joke.objects.filter(id=pk, added_by=request.user)
        joke_resp = joke[0]
        if joke:
            joke.delete()
        else:
            raise Http404("No such joke")
        return HttpResponse(f"Removed joke: {joke_resp}")


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


update_joke = csrf_exempt(UpdateJokeView.as_view())
remove_joke = csrf_exempt(RemoveJokeView.as_view())
