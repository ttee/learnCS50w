from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"), 
    path("listings/<str:listid>", views.listing_detail, name="listing_detail"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closed_listing", views.closed_listing, name="closed_listing"),
    path("listing_categories", views.listing_categories, name="listing_categories"),
    path("same_category/<str:item_category>", views.same_category, name="same_category"),
]
