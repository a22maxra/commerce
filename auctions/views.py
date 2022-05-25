from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import Category, User, Listing, Bid, Comment, Watch

class ListForm(forms.Form):
    # Load all the categories to select dropdown
    categories = []
    allCategories = Category.objects.all()
    for i in allCategories:
        categories.append((i.id, i.category))
    title = forms.CharField(label="Titel", max_length=125)
    description = forms.CharField(label="Description", max_length=280)
    category = forms.ChoiceField(widget=forms.Select,
    choices=categories)
    image = forms.CharField(label="Image", max_length=280)
    start = forms.IntegerField(label="Starting price", min_value=0)



def index(request):
    return render(request, "auctions/index.html")


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


def create(request):
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            listing = form.cleaned_data
            u = User.objects.get(pk=request.user.id)
            c = Category.objects.get(pk=int(listing["category"]))
            l = Listing(title=listing["title"], description=listing["description"],
            image=listing["image"], start=int(listing["start"]), lister=u)
            l.save()
            l.category.add(c)
            print(listing)
    return render(request, "auctions/create.html", {
    "form": ListForm()
    })