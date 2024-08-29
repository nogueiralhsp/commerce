from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    def __repr__(self):
        return self.username
    
    def __unicode__(self):
        return self.username

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winning_listings", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title
    
    def __unicode__(self):
        return self.title
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.listing.title}"
    
    def __repr__(self):
        return f"{self.user.username} bid {self.amount} on {self.listing.title}"
    
    def __unicode__(self):
        return f"{self.user.username} bid {self.amount} on {self.listing.title}"
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.listing.title}"
    
    def __repr__(self):
        return f"{self.user.username} commented on {self.listing.title}"
    
    def __unicode__(self):
        return f"{self.user.username} commented on {self.listing.title}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user.username} is watching {self.listing.title}"
    
    def __repr__(self):
        return f"{self.user.username} is watching {self.listing.title}"
    
    def __unicode__(self):
        return f"{self.user.username} is watching {self.listing.title}"
    
class category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def __unicode__(self):
        return self.name