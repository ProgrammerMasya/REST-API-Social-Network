from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from home.forms import LoginForm, PostsForm, RegistrationForm
from home.models import Dislike, Like, Post


class PostsView(TemplateView):
    def get(self, request):
        form = PostsForm()
        posts = Post.objects.all().order_by("-created")
        context = {"form": form, "posts": posts}
        return render(request, "posts.html", context)

    def post(self, request):
        form = PostsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form = PostsForm()
            return HttpResponseRedirect(reverse("base"))

        context = {"form": form}
        return render(request, "posts.html", context)


def like_view(request):
    dislikes = Dislike.objects.filter(post=request.POST.get("post_id"), user=request.user)
    likes = Like.objects.filter(post=request.POST.get("post_id"), user=request.user)
    post = Post.objects.get(pk=request.POST.get("post_id"))
    if not likes:
        if dislikes:
            dislike = Dislike.objects.get(
                post=request.POST.get("post_id"), user=request.user
            )
            dislike.delete()
            post.dislikes -= 1
        Like.objects.create(post=post, user=request.user)
        post.likes += 1
        post.save()
    return HttpResponseRedirect(reverse("base"))


def dislike_view(request):
    dislikes = Dislike.objects.filter(post=request.POST.get("post_id"), user=request.user)
    likes = Like.objects.filter(post=request.POST.get("post_id"), user=request.user)
    post = Post.objects.get(pk=request.POST.get("post_id"))
    if not dislikes:
        if likes:
            like = Like.objects.get(post=request.POST.get("post_id"), user=request.user)
            like.delete()
            post.likes -= 1
        Dislike.objects.create(post=post, user=request.user)
        post.dislikes += 1
        post.save()
    return HttpResponseRedirect(reverse("base"))


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse("home"))
    context = {"form": form}
    return render(request, "registration.html", context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse("base"))
    context = {"form": form}
    return render(request, "login.html", context)


def profile_view(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    context = {"user": user}
    return render(request, "profile.html", context)
