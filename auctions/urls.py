from django.urls import path

from . import views

urlpatterns = [
    # index view
    path("", views.index, name="index"),
    # user views
    path("user_login", views.login_view, name="user_login"),
    path("user_logout", views.logout_view, name="user_logout"),
    path("user_register", views.register_view, name="user_register"),

    # listing views
    path("listing_create", views.listing_create_view, name="listing_create"),
    path("listing_view/<int:listing_id>", views.listing_view, name="listing_view"),
    path("listing_edit/<int:listing_id>", views.listing_edit_view, name="listing_edit"),
    path("listing_toggle_active/<int:listing_id>", views.listing_toggle_active_view, name="listing_toggle_active"),

    # bid and comment views
    path("bid_create/<int:listing_id>", views.create_bid_view, name="bid_create"),
    path("comment_create/<int:listing_id>", views.create_comment_view, name="comment_create"),
    path("watchlist_toggle/<int:listing_id>", views.watchlist_toggle_view, name="watchlist_toggle"),
]