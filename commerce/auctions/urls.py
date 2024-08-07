from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("profile", views.profile, name="profile"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.display_catagory, name="category"),
    
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/edit", views.edit, name="edit"),
]
