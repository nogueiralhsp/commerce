from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist

# index view
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


################### users ###################
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
            return render(request, "auctions/user_login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/user_login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/user_register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/user_register.html")


################### listings ###################
def listing_create_view(request):

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        user = request.user

        # Attempt to create new listing
        try:
            listing = Listing.objects.create(
                title=title,
                description=description,
                starting_bid=starting_bid,
                image_url=image_url,
                category=category,
                user=user
            )
            listing.save()
        except IntegrityError:
            return render(request, "auctions/listing_create.html", {
                "message": "Error creating listing."
            })
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/listing_create.html")

def listing_view(request, listing_id, user=None):
    listing = Listing.objects.get(pk=listing_id)
    current_bid = biggest_bid(listing_id)

    return render(request, "auctions/listing_view.html", {
        "listing": listing,
        "current_bid": current_bid,
        "comments": listing.comments.all().order_by('-created'),
    })

def listing_edit_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        listing.title = request.POST["title"]
        listing.description = request.POST["description"]
        listing.starting_bid = request.POST["starting_bid"]
        listing.image_url = request.POST["image_url"]
        listing.category = request.POST["category"]
        listing.save()
        return HttpResponseRedirect(reverse('listing_view', args=(listing_id,)))
    elif request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        return render(request, "auctions/listing_edit.html", {
            "listing": listing
        })

    return render(request, "auctions/listing_edit.html", listing_id)

def listing_toggle_active_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = not listing.active
    print (f'listing.active: {listing.active}')
    listing.save()
    return redirect('listing_view', listing_id=listing_id)

################### Biddings ###################
def biggest_bid (listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = listing.bids.all()
    if len(bids) == 0:
        return listing.starting_bid
    else:
        return max(bids, key=lambda x: x.amount).amount

def create_bid_view(request, listing_id):
    # making sure the request is a POST request
    if request.method == "POST":
        # creating variables for the bid and the listing
        bid=float(request.POST["bid"])
        listing = Listing.objects.get(pk=listing_id)
        user = request.user

        # making sure the bid is greater than the current bid
        if bid <= float(biggest_bid(listing_id)):
                return render(request, "auctions/listing_view.html", {
                    "listing": listing,
                    "current_bid": biggest_bid(listing_id),
                    "message": f"Bid must be greater than current bid."
                })
        else:
            # Attempt to create new bid
            try:
                bid = Bid.objects.create(
                    listing=listing,
                    user=user,
                    amount=bid
                )
                bid.save()
                return (HttpResponseRedirect(reverse('listing_view', args=(listing_id,))))
                
            except IntegrityError:
                return render(request, "auctions/bid_create.html", {
                    "message": "Error creating bid."
                })

################### Comments ###################
def create_comment_view (request, listing_id):
    # making sure the request is a POST request
    if request.method == "POST":
        # creating variables for the comment and the listing
        comment=request.POST["comment"]
        listing = Listing.objects.get(pk=listing_id)
        user = request.user

        # Attempt to create new comment
        try:
            comment = Comment.objects.create(
                listing=listing,
                user=user,
                comment=comment
            )
            comment.save()
            return HttpResponseRedirect(reverse('listing_view', args=(listing_id,)))
        except IntegrityError:
            return render(request, "auctions/listing_view.html", {
                "message": "Error creating comment."
            })
        
################### Watchlist ###################
def watchlist_toggle_view(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        watchlist = Watchlist.objects.filter(user=user, listing=listing)
        if watchlist:
            watchlist.delete()
        else:
            watchlist = Watchlist.objects.create(
                user=user,
                listing=listing
            )
            watchlist.save()
        return HttpResponseRedirect(reverse('listing_view', args=(listing_id,)))
    return HttpResponseRedirect(reverse('index'))