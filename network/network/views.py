import json
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Post
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.user.is_authenticated:
        return render(request, "network/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))

def profile(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(id = user_id)
        profile_user_id = user.id
        profile_username = user.username
             
        following_list = [x.id  for x in user.following.all()]
        followers_list = [x.id  for x in user.followers.all()]


        context = {
            "following": following_list, 
            "followers": followers_list, 
            "profile_user_id": profile_user_id,
            "profile_username": profile_username,
        }
        print(context)
        return render(request, "network/index.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))

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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def refresh_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        #read the content of the request and save the request into the database
        author = request.user
        content = data['content']
        post = Post(
            author=author,
            content=content,
        )
        post.save()
        print('saved success')
        return JsonResponse({"message": "Post sent successfully."}, status=201)
    if request.method == "GET":
        posts = Post.objects.all().order_by('-timestamp')
        # create a paginator for posts
        paginator = Paginator(posts, 10)
        # if page not provided in request, return the latest page
        page_number = request.GET.get('page')
        print(page_number)
        page_obj = paginator.get_page(page_number)

        ser_posts = [post.serialize() for post in page_obj] 
        
        #serialize function returns a dictionary, serialize function is defined in models.py
        #so post.serialize() returns a dictionary for each post in posts. this becomes a list of dictionaries
        #then we return to JsonResponse a dictionary with key "posts" pointing to a list of dictionaries
        
        # create a context that contains
        # posts
        # attributes of the paginator
        context = {
            "posts": ser_posts,
            "page_obj": {
                "has_previous": page_obj.has_previous(),
                "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous()  else page_obj.number,
                "number": page_obj.number,
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
                "next_page_number": page_obj.next_page_number() if page_obj.has_next()  else page_obj.number,
            }
        }
        return JsonResponse(context, status=201)

def refresh_user_post(request, user_id):

    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(
        author=user, 
    )

    ser_posts = [post.serialize() for post in posts] 

    #serialize function returns a dictionary, serialize function is defined in models.py
    #so post.serialize() returns a dictionary for each post in posts. this becomes a list of dictionaries
    #then we return to JsonResponse a dictionary with key "posts" pointing to a list of dictionaries
    return JsonResponse({"posts": ser_posts}, status=201)

# add a view for following posts
def refresh_following_posts(request):

    # this current user is the request user
    # get all users that current user is following
    # for each such user, get all posts
    # combine all the posts together (sorted) and return as Json reponse
    requestuser = User.objects.get(id=request.user.id)

    print(request.user.id)
    print(requestuser)
    all_following_users = requestuser.following.all()
    listfollowingpost = []
    for user in all_following_users:
        posts = Post.objects.filter(
            author=user, 
        )
        listfollowingpost.extend(posts)

    ser_posts = [post.serialize() for post in listfollowingpost] 
    print(ser_posts)

    #serialize function returns a dictionary, serialize function is defined in models.py
    #so post.serialize() returns a dictionary for each post in posts. this becomes a list of dictionaries
    #then we return to JsonResponse a dictionary with key "posts" pointing to a list of dictionaries
    return JsonResponse({"posts": ser_posts}, status=201)
 

def update_user_following(request, followed_user):

    # is followed_user already followed by current_user?

    # currentuser A is the user that wants to follow B
    # so check if B.followers has A
    # request.user = A, followed_user = B
    # check if request.user.username is in followed_user.followers
    # A is in B.followers OR
    # B is in A.following

    A = User.objects.get(id=request.user.id)
    B = User.objects.get(id=followed_user)

    print(A.following.all())
    if B in A.following.all():
        # if yes: remove from current_user's following
        # B.followers.remove(A)
        A.following.remove(B)
    else:
        # B.followers.add(A)
        A.following.add(B)
    print(A.following.all())
    # if no: add to current_user's following
    # return success status
    B.save()
    print("Saved B")
    A.save()
    print("Saved A")
    return JsonResponse({"message": "FollowButton clicked successfully."}, status=201)