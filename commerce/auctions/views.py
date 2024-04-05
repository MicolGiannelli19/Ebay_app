# authetification inports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms

# Model imports
from .models import User, Listing, Comment, Bid


def profile(request):
    return render(request, "auctions/profile.html", {"user": request.user})


def index(request):
    return render(request, "auctions/index.html", {"listings": Listing.objects.all()})


#  NOTE sure what method is best probably the one bellow

# class ListingForm(forms.Form):
#     title = forms.CharField(label="Title")
#     description = forms.CharField(label="Description")
#     starting_bid = forms.DecimalField(label="Starting Bid")
#     image_url = forms.URLField(label="Image URL", required=False)
#     category = forms.CharField(label="Category", required=False)


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "starting_bid",
            "image",
            "category",
            "user",
            "intrested_users",
            "active",
        ]


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


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = listing.comments.all()
    bids = listing.bids.all()
    return render(
        request,
        "auctions/listing.html",
        {"listing": listing, "comments": comments, "bids": bids},
    )


@login_required()
def watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        user = request.user
        user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# TODO: change it to be a django form
@login_required()
def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(id=listing_id)
        text = request.POST["comment"]
        comment = Comment(user=user, listing=listing, text=text)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
