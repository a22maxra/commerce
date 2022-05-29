from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=32)
    def __str__(self):
        return self.category


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=280)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="Categories")
    image = models.CharField(max_length=280, blank=True, null=True)
    start = models.IntegerField()
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    status = models.BooleanField(default = True)
    def __str__(self):
        return str(self.id)

class Bid(models.Model):
    offer = models.IntegerField()
    bid_item = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="BidItems")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    def __str__(self):
        return str(self.offer)


class Comment(models.Model):
    message = models.CharField(max_length=280)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    comment_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="CommentItems")
    

class Watch(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Watching")
    watcher =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="Watchers")
