from copy import error
from unicodedata import name
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Category, User, Auction, Bet, Comment
from django.db.models import Max

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(active=True),
        "main_page": "underline"
    })

@login_required
def auctions_history(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        "history": True,
        "history_page": "underline"
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
                "message": "Invalid username and/or password.",
                "enter_page": "underline"
            })
    else:
        return render(request, "auctions/login.html", {"enter_page": "underline"})


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
                "message": "Passwords must match.",
                "sign_up_page": "underline"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "sign_up_page": "underline"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {"sign_up_page": "underline"})

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "category_page": "underline"
    })

def auction(request, category, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    bets = auction.bet.all()
    if bets:
       max_bet = bets.aggregate(Max("stuffBet")).get('stuffBet__max')
    else:
        max_bet = auction.initialPrice
    # category = Auction.category.get(id=auction_id)
    comments = Comment.objects.filter(stuff=auction)
    if request.user.is_authenticated:
       user = request.user
       if user == auction.author:
            author_auction = True
       else:
            author_auction = False 
       if user == auction.winner:
          winner_user = True
       else:
          winner_user = False
       in_watchlist = user.watch_list.filter(pk=auction_id)
       if in_watchlist:
            return render(request, "auctions/auction.html", {
            "auction": auction,
            "max_bet": max_bet,
            "switch": False,
            "bets": bets,
            "comments": comments,
            "author_auction": author_auction,
            "winner_user": winner_user  
            })
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "max_bet": max_bet,
        "switch": True,
        "comments": comments,
        "author_auction": False
    })

def category(request, category):
    category = Category.objects.get(name = category)
    auctions = category.auctions.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "category": category,
        "switch": True     
    })

@login_required
def watchlist(request):
    user = request.user
    auctions = user.watch_list.all()
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions,
        "watchlist_page": "underline"
    })


@login_required
def to_watchlist(request, category, auction_id):
    if request.method == "POST":
        user = request.user
        auction_id = request.POST["auction"]
        auction = Auction.objects.get(pk=auction_id)
        auction.watchlist.add(user)
        return HttpResponseRedirect(reverse("auction", kwargs={"category":category, "auction_id": auction_id}))

@login_required
def del_from_watchlist(request, category, auction_id):
    if request.method == "POST":
        user = request.user
        auction_id = request.POST["auction"]
        auction = Auction.objects.get(pk=auction_id)
        auction.watchlist.remove(user)
        return HttpResponseRedirect(reverse("watchlist"))

@login_required
def create_auction(request):
    if request.method == "POST":
        nameStuff = request.POST["nameStuff"]
        descriptionStuff = request.POST["descriptionStuff"]
        initialPrice = request.POST["initialPrice"]
        category = request.POST["category"]
        imageStuff = request.FILES["imageStuff"]
        user = request.user
        f = Auction(nameStuff = nameStuff, 
                    descriptionStuff = descriptionStuff, 
                    initialPrice = initialPrice, 
                    category = Category.objects.get(pk = category), 
                    imageStuff = imageStuff,
                    author = user)         
        f.save()
        f.watchlist.add(user)
        return render(request, "auctions/auction.html", {
        "auction": f,
        "switch": False
    })
    return render(request, "auctions/create_auction.html", {
        "error": error,
        "categories": Category.objects.all(),
        "create_page": "underline"
    })



@login_required
def bet(request, category, auction_id):
    if request.method =="POST":
        user = request.user
        bet_number = request.POST["bet_number"]
        f = Bet(userName = user, 
        stuff = Auction.objects.get(pk=auction_id),
        stuffBet = bet_number)
        f.save()
        return HttpResponseRedirect(reverse("auction", kwargs={"category":category, "auction_id": auction_id}))




@login_required
def comment(request, category, auction_id):
    if request.method =="POST":
        user = request.user
        comment_text = request.POST["comment_text"]
        t = Comment(userName = user,
        stuff = Auction.objects.get(pk=auction_id),
        commentText = comment_text)
        t.save()
        return HttpResponseRedirect(reverse("auction", kwargs={"category":category, "auction_id": auction_id}))


@login_required
def close(request, category, auction_id):
    if request.method == "POST":
        auction_id = request.POST["close"]
        auction = Auction.objects.get(pk=auction_id)
        auction.active = False
        auction.closeDatetime = timezone.now()
        auction.winner = Bet.objects.filter(stuff=auction).last().userName
        auction.save()
        return HttpResponseRedirect(reverse("index"))


@login_required
def achievements(request):
    user = request.user
    auctions = Auction.objects.filter(winner = user)
    return render(request, "auctions/achievements.html", {
        "auctions": auctions,
        "achievement_page": "underline"
    })








        