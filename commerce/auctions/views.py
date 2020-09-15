        # itemlist = [] #list have method append
        # for query in watchlist.all():
        #     itemlist.append(query.id)
#list is an ordered data structure, so we have append for lists
#set is unique, unordered data structure, so we have add for sets
# if i type itemlist = itemlist.append(variable)
# append function return value is NONE, so itemlist will always be assigned value of NONE.
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, AuctionListing, Bid, Comment

class NewListingForm(forms.Form):
    image_link= forms.CharField()
    item_title= forms.CharField()
    item_category= forms.CharField()
    item_price= forms.IntegerField()
    item_desc= forms.CharField()

class SubmitBidForm(forms.Form):
    price= forms.IntegerField(widget=forms.HiddenInput(), initial=0)

class commentForm(forms.Form):
    comment= forms.CharField()

def index(request):
    # in index.html, get from models.AuctionListing
    # display in index.html extend layout.html in block body

    if request.method == "GET":
        #breakpoint()
        context = {'listings':AuctionListing.objects.filter(item_status = 'Active')}
    return render(request, "auctions/index.html", context)

def listing_categories(request):
    # in index.html, get from models.AuctionListing
    # display in index.html extend layout.html in block body

    if request.method == "GET":
        #breakpoint()
        context = {'listings':AuctionListing.objects.filter(item_status = 'Active')}
        items = context['listings']
        list_set =set()
        for item in items:
            list_set.add(item.item_category)
        conttext = {'list_set':list(list_set)}
        conttext = {'list_set':['Apple','kjkkj']}
        #breakpoint()
    return render(request, "auctions/listing_categories.html", conttext)

def same_category(request, item_category):
    # in index.html, get from models.AuctionListing
    # display in index.html extend layout.html in block body

    if request.method == "GET":
        #breakpoint()
        context = {'listings':AuctionListing.objects.filter(item_category = item_category)}
    return render(request, "auctions/same_category.html", context)

def closed_listing(request):
    # in index.html, get from models.AuctionListing
    # display in index.html extend layout.html in block body

    if request.method == "GET":
        #breakpoint()

#winner, winning_bid
#i know the AuctionListing items to be displayed
# the price is related to these items in a different table Bid
# if i call the Auctionlisting items, the bid price should automatically be called somehow using the relationship
# get the bid price from Bid table using the listitem id

    # how do you get the winning bid for each item?
    # winning_bid is not in the model AuctionListing
    # -> 
        context = {'listings':AuctionListing.objects.filter(item_status = 'InActive')}
    return render(request, "auctions/closed_listing.html", context)


def listing_detail(request, listid):
    #get request from activelisting page
    #show listing_detail in template file
    #get an instance of the AuctionListing class from the database
    #classname.objects.getmethodfromDB(where id=parameter)
    listitem = AuctionListing.objects.get(id=listid) 
    owner = listitem.list_user #access the current object (instance of auctionListing)

    watchlist= None
    itemlist = None
    pricelist =[]
    error = None
    
    #submitBidform = None
    isOwnerCheck = None

    # when user select individual listing, listing_detail template shows the listing 
    # check if user is login to see which button to display
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)   #user on the page, may not be owner
        # User model has attribute watchlist (whatlist is created automatically by related_name)
 
        isOwnerCheck = user.id == owner.id

        watchlist = user.watchlist
        itemlist = [query.id for query in watchlist.all()] #convert the watchlist object into a list of id #list comprehensive

    if request.method=="GET":
        return render(request, "auctions/listing_detail.html", {
            'listitem':listitem,
            'watchlist':itemlist,
            'SubmitBidForm':SubmitBidForm(initial={'price':''}), #submitbidform is created
            'isOwnerCheck': isOwnerCheck,
            'commentForm':commentForm(),
            'comments':listitem.comments.all(),
        })

    if request.method=="POST":
        commentform = commentForm(request.POST)
        submitBidform = SubmitBidForm(request.POST)
        breakpoint()
        # breakpoint()
        if "Remove_key" in request.POST:
            watchlist.remove(listitem.id)
        elif "CommentButton" in request.POST:
            if commentform.is_valid():
                comment_content = commentform.cleaned_data['comment']
                comment = Comment(
                    content = comment_content,
                    author = user,
                    item = listitem,
                )
                comment.save()
                #check if bid is empty or not
                #display bid in render

            print(comment)
            # comment -> str
            # comment.__repr__()
            # comment.__str__()
            commentform = commentForm()
            
        elif "Watchlist" in request.POST:
            watchlist.add(listitem.id)
        elif "BidButton" in request.POST:
            #submitBidform = SubmitBidForm(request.POST)
            if submitBidform.is_valid():
                price = submitBidform.cleaned_data['price']
                listitem = AuctionListing.objects.get(id=listid)
                allBidsForItem = listitem.bids.all()
                for x in allBidsForItem:
                    pricelist.append(x.bid_price)
                max_price = max(pricelist, default=0)
                if price > max_price:
                    pricelist.append(price)
                    thisBid = Bid(
                        list_item= listitem,
                        bid_price=price, 
                        bid_user=user, 
                        )
                    thisBid.save()
                    error = "Your Bid is accepted."
                    submitBidform = SubmitBidForm()
                else:
                    error = "The Bid is too small. Please enter a higher bid."
        else: # Close Bid
            print("Closing bid")            
            listitem.item_status = 'InActive'

            # winning_bid = listitem.bids[0]
            # for bid in listitem.bids:
            #     if bid.bid_price > winning_bid.price:
            #         winning_bid = bid
            # winner = winning_bid.bid_user

            winning_bid = max(listitem.bids.all(), key=lambda bid: 0 if bid is None else bid.bid_price, default=None)
            if winning_bid is not None:
                winner = winning_bid.bid_user
                print(winner.id)
                listitem.winner = winner
                listitem.winning_price = winning_bid.bid_price
            listitem.save()

        itemlist = [query.id for query in watchlist.all()] #convert the watchlist object into a list of id #list comprehensive

        #get all bids where bid item id = current item id
        
        #get id of current item which is listitem.id
        # target: get all the bids from a specific item
        # 1. use the bid table:
        # go throught every row, for each row look for list_item equal to listitem.id
        
        # 2. use the AuctionListing table:
        # find the specific row with id listitem.id
        # in that row, get all bids
        return render(request, "auctions/listing_detail.html", {
            'listitem':listitem,
            'watchlist':itemlist,
            'number_of_bids': len(pricelist),
            'error': error,
            'SubmitBidForm': submitBidform, #submitbidform with data is posted to server
            'isOwnerCheck': isOwnerCheck,
            'commentForm':commentform,
            'comments':listitem.comments.all(),
        })




def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)          
            Auc_listing = AuctionListing(
                list_user= user,
                image_link=form.cleaned_data['image_link'], 
                item_title=form.cleaned_data['item_title'], 
                item_category=form.cleaned_data['item_category'], 
                item_price=form.cleaned_data['item_price'], 
                item_desc=form.cleaned_data['item_desc'],
                item_status='Active',
                )
            Auc_listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create_listing.html", {
            "form": NewListingForm()
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

def watchlist(request):
    # using User table
    # find the specific user
    #  in that row , get all the items in watchlist
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)   
    if request.method == "GET":
        context = {'watchlist':user.watchlist.all()}
    return render(request, "auctions/watchlist.html", context)