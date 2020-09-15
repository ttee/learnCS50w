from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name="watched_by")

# check if user is login
# if user is login, get a watchlist that belongs to user
# if user clicks on watchlist at listing_detail.html, then append watchlist with listitem object
# when appending listitem object, check that the session is not CSRF using default CSRF code
# how related_name attribute works:
# watchlist is a column in the user table
# and each row in the watchlist column contains a list of all the items

class AuctionListing(models.Model):
    image_link= models.CharField(max_length=100)
    item_title= models.CharField(max_length=100)
    item_category= models.CharField(max_length=200)
    item_price= models.IntegerField(max_length=10)
    list_datetime= models.DateTimeField(auto_now_add=True, blank=True)
    list_user= models.ForeignKey(User, on_delete=models.CASCADE)
    item_desc= models.TextField(max_length=200)
    item_status = models.TextField(max_length=10, blank = True)
    winner= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="won_items")
    winning_price =   models.IntegerField(max_length=10, blank=True, null=True)
    # winning_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True)


# User table
# ---------------
# id, won_items
# 1 [1, 2]
# 2 [3]

# AuctionListing table
# id, winner, winning_bid
# 1, 1, 1
# 2, 1, 3
# 3, 2, None

# Bid table
# id, item_id, price
# 1 1 4
# 2 2 5
# 3 2 8
class Bid(models.Model):
    list_item= models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, related_name="bids")
    bid_price= models.IntegerField(max_length=10)
    bid_datetime= models.DateTimeField(auto_now_add=True, blank=True)
    bid_user= models.ForeignKey(User, on_delete=models.CASCADE)

#the Bid model allows me to store a list of bids and the associated bid details

class Comment(models.Model):
    content= models.TextField()
    item= models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, related_name="comments")
    createddatetime= models.DateTimeField(auto_now_add=True, blank=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE)