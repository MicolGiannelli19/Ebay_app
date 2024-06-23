# authetification inports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django import forms

# TODO: find out where to put error handling if user is not logged in
# Model imports
from .models import User, Listing, Comment, Bid



# Models defenitions

def profile(request):
    return render(
        request,
        "auctions/profile.html",
        {
            "user": request.user,
            "watchlist": request.user.watchlist.all(),
            "bids": request.user.bids.all(),
            "listings": request.user.listings.all(),
        },
    )


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "starting_bid",
            "image",
            "category",
        ]


# User Managment 

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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#  Basic Functionality views 

def index(request):
    message = request.GET.get("message", "")
    return render(
        request,
        "auctions/index.html",
        {"listings": Listing.objects.all(), "message": message},
    )

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = listing.comments.all()
    bid = listing.bids.all().last()
    message = request.GET.get("message", "")
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "message": message,
            "comments": comments,
            "highest_bid": bid,
            "bid_form": BidForm(),
        },
    )



# Actions that can be Made to a listing

@login_required()
def watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        user = request.user
        if user.watchlist.filter(id=listing_id).exists():
            user.watchlist.remove(listing)
            message = "Removed from watchlist"
        else:
            message = "Added to watchlist"
            user.watchlist.add(listing)

        new_url = reverse("listing", args=(listing_id,))
        return HttpResponseRedirect(new_url + "?message=" + message)
    else:
        return HttpResponseRedirect(
            reverse("listing", args=(listing_id,)) + "?message=Invalid request"
        )


@login_required()
def bid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            user = request.user
            listing = Listing.objects.get(id=listing_id)
            if listing.bids.all().count() > 0:
                current_bid = listing.bids.all().last().amount
            else:
                current_bid = listing.starting_bid
            if amount > current_bid:
                bid = Bid(amount=amount, user=user, listing=listing)
                bid.save()
                return HttpResponseRedirect(
                    reverse("listing", args=(listing_id,)) + "?message=Bid added"
                )
    return HttpResponseRedirect(
        reverse("listing", args=(listing_id,)) + "?message=Invalid request"
    )


@login_required()
def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(id=listing_id)
        text = request.POST["comment"]
        comment = Comment(user=user, listing=listing, text=text)
        comment.save()
        return HttpResponseRedirect(
            reverse("listing", args=(listing_id,)) + "?message=Comment added"
        )
    else:
        return HttpResponseRedirect(
            reverse("listing", args=(listing_id,)) + "?message=Invalid form data"
        )



@login_required()
def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            # TODO: look up the model forms to do this more efficently
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            user = request.user
            listing = Listing(
                title=title,
                description=description,
                starting_bid=starting_bid,
                image=image,
                category=category,
                user=user,
                active=True,
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/new_listing.html",
                {"form": form, "message": "Invalid form data"},
            )
    else:
        form = ListingForm()
        return render(request, "auctions/new_listing.html", {"form": form})


# Changes to personal active listing
@login_required()
def edit(request, listing_id):
    # NOTE: Bettrer design for this would be making edit and new page call the same thing and submit it diffrently based on if it exists or not 

    # Take the newly submitted from and change the ingotmation in the database
    if request.method == "POST":
        # form = ListingForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
        return HttpResponse("form was not valid")
    else:
        listing_obj = Listing.objects.get(id=listing_id)
        old_form = ListingForm(instance=listing_obj)
        
        return render(
            request, "auctions/edit.html", {"listing_id": listing_id, "form": old_form}
        )

@login_required()
def close(request, listing_id):
    if request.method == "POST":
        if request.user != Listing.objects.get(id=listing_id).user:
            return HttpResponse("ERROR: Cannot close listing, you are not the owner!!")
        listing = Listing.objects.get(id=listing_id)
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
