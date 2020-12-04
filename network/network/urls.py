
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>", views.profile, name="profile"),
    

    # API Routes
    path("posts", views.refresh_post, name="refresh_post"),
    # add route for following posts
    path("posts/following", views.refresh_following_posts, name="refresh_following_posts"),
    path("users/<int:user_id>/posts", views.refresh_user_post, name="refresh_user_post"),
    path("follows/<int:followed_user>", views.update_user_following, name="update_user_following")
    # the endpoint 'posts' is an address in the server that points to the views.refresh_post function
    # the url is for interacting with user
    # the views is for interacting with controller logic
    # the name is for interacting with the template
    # 'refresh_post' is the variable name of the url
    # 'posts' is an url (i.e. address) in the server 
    # 'views.new_post' is the function (i.e. block of code)
]
