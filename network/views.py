import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator

from .models import *

#import all ModelForm
from .forms import *

def index(request):

    if request.method == "POST":
        f = NewPostForm(request.POST)
        if f.is_valid():
            instance = f.save(commit=False)
            instance.user = request.user
            instance.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        all_posts = NewPost.objects.order_by("-date")
        f = NewPostForm()

        # Paginator
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "NewPostForm": f,
            "page_obj": page_obj,
            "num_pages": range(paginator.num_pages)
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            profile = Profile.objects.create(user_id=user.id)
            profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, profile_username):

    # Gets currently logged in user
    user = request.user

    # Gets visited profile
    visited_profile = User.objects.get(username=profile_username)

    # Gets posts and returns them in reverse order (oldest first)
    posts = NewPost.objects.filter(user_id=visited_profile.id).order_by("-date")

    profile = Profile.objects.get(user_id=visited_profile.id)
    my_profile = Profile.objects.get(user_id=user.id)

    # Follow functionality
    if request.method == "POST":

        # Check if 'profile' already is followed by 'my_profile'. If already following, remove, else add.
        if profile.followed_by.filter(id=my_profile.id).exists():
            profile.followed_by.remove(my_profile)
        else:
            profile.followed_by.add(my_profile)

        return HttpResponseRedirect(reverse("profile", args=(profile_username,)))

    # Using this bool to determine whether a user is following the visited profile
    following_bool = profile.followed_by.filter(id=my_profile.id).exists()

    # Counting number of followers
    followers_no = profile.followed_by.all().count()

    return render(request, "network/profile.html", {
        'posts': posts,
        'profile': visited_profile,
        'following_bool': following_bool,
        'followers_no': followers_no
    })

def following(request):

    # Get current profile
    current_profile = Profile.objects.get(id=request.user.id)

    # Get followed users
    followed_users = Profile.objects.filter(followed_by=current_profile)

    # Empty QuerySet receives all relevant posts
    p = NewPost.objects.none()
    for user in followed_users:
        p = p | NewPost.objects.filter(user_id=user.id).order_by("-date")

    return render(request, "network/following.html", {
        "posts": p
    })

@csrf_exempt
def savepost(request, id):
    post = NewPost.objects.get(id=id, user=request.user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        post.post_text = data["post_text"]
        post.save()
        return HttpResponse(status=204)
        
