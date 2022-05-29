from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max
from django.contrib.auth.decorators import login_required


from .forms import ListingForm, BidForm, CommentForm

from .models import Category, User, Listing, Bid, Comment, Watch

class WatchForm(forms.Form):
    # Load all the categories to select dropdown
    field = forms.CharField(initial='watch', widget = forms.HiddenInput(), required = False)


class CloseForm(forms.Form):
    # Load all the categories to select dropdown
    field = forms.CharField(initial='close', widget = forms.HiddenInput(), required = False)


def index(request):
    listings = Listing.objects.filter(status=True)
    bids = []
    for listing in listings:
        try:
            bid = listing.BidItems.latest('offer')
            bids.append(bid)
        except:
            bid = None
            bids.append(bid)
    print(bids)
    count = 1
    stitch = zip(listings, bids)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "bids": bids,
        "count": count,
        "stitch": stitch,
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
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
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        # Save and add new listing to database
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.cleaned_data
            print(listing["category"])
            u = User.objects.get(pk=request.user.id)
            c = Category.objects.get(category=listing["category"])
            l = Listing(title=listing["title"], description=listing["description"],
            image=listing["image"], start=int(listing["start"]), lister=u, category=c)
            l.save()
            list_id = Listing.objects.latest('id').id
            return HttpResponseRedirect(reverse("listing", args=[list_id]))
    return render(request, "auctions/create.html", {
    "form": ListingForm(),
    })


@login_required(login_url='/login')
def listing(request, listing_id):
    u = User.objects.get(pk=request.user.id)
    l = Listing.objects.get(pk=listing_id)

    # Load this listings bid            
    bid = None
    minBid = 0
    try:
        bid = l.BidItems.latest('offer')
        minBid = int(bid)
    except:
        minBid = int(l.start)

    bidError = ""
    if request.method == "POST":

    # Validate bid and add or display error
        form = BidForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if minBid < form["offer"]:
                newBid = Bid(offer=form["offer"], bid_item=l, bidder=u)
                newBid.save()
                bid = l.BidItems.latest('offer')
            else:
                bidError = "Your bid must be greater than current bid by 1$"
        
        # Add comment
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            newComment = Comment(message=form["message"], commenter=u,comment_item = l)
            newComment.save()
            print(newComment)

        # Add listing to watchlist
        else:
            form = WatchForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                print(form)
                if form["field"] == "watch":
                    try:
                        watch = Watch.objects.get(item = l, watcher = u)
                        watch.delete()
                        print("Deleted")
                    except:
                        watch = Watch(item=l, watcher=u)
                        watch.save()
                        print("Saved")

                # Close auction
                if form["field"] == "close":
                    if l.status:
                        l.status = False
                        l.save()
                    else:
                        l.status = True
                        l.save()
            
    # If listing is in watchlist, load another class for button
    try:
        watch = Watch.objects.get(item = l, watcher = u)
        buttonClass = "m-1 btn btn-info"
    except:
        buttonClass = "m-1 btn btn-secondary"

    # Owner of auction has a "close" option
    if l.lister.id == request.user.id:
        if l.status:
            buttonClassClose = "m-1 btn btn-warning"
        else:
            buttonClassClose = "m-1 btn btn-danger"
        return render(request, "auctions/listing.html", {
            "listing": l,
            "bid": bid,
            "form": BidForm,
            "form1": WatchForm(),
            "formClose": CloseForm,
            "formComment": CommentForm,
            "owner": 1,
            "buttonClass": buttonClass,
            "buttonClassClose": buttonClassClose,
            "bidError": bidError,
            "comments": Comment.objects.filter(comment_item=l)
        })

    return render(request, "auctions/listing.html", {
        "listing": l,
        "bid": bid,
        "form": BidForm,
        "form1": WatchForm(),
        "formComment": CommentForm,
        "owner": None,
        "buttonClass": buttonClass,
        "bidError": bidError,
        "comments": Comment.objects.filter(comment_item=l)
    })


@login_required(login_url='/login')
def watchlist(request):
    listings = []
    watching = Watch.objects.filter(watcher = request.user)
    for watch in watching:
        listings.append(watch.item)
    bids = []
    for listing in listings:
        try:
            bid = listing.BidItems.latest('offer')
            bids.append(bid)
        except:
            bid = None
            bids.append(bid)
    print(bids)
    count = 1
    stitch = zip(listings, bids)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "bids": bids,
        "count": count,
        "stitch": stitch,
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def category(request, category):
    ctg = Category.objects.get(category=category)
    print(ctg)
    listings = ctg.Categories.all()
    print(listings)
    bids = []
    for listing in listings:
        print(listing.status)
        try:
            bid = listing.BidItems.latest('offer')
            bids.append(bid)
        except:
            bid = None
            bids.append(bid)
    print(bids)
    stitch = zip(listings, bids)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "bids": bids,
        "stitch": stitch,
    })