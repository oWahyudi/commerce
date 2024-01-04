from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):   
    def __str__(self):
        return str(self.username)

# Category - Managed by Administrator
class Category(models.Model):
    name=models.CharField(max_length=255, verbose_name='Category Name')  

    def __str__(self):
        return self.name


#Auction Listing
class AuctionList(models.Model):
    categoryid=models.ForeignKey(Category, related_name='CategoryAuctionList', null=True,blank=True, on_delete=models.RESTRICT, verbose_name='Category')
    title=models.CharField(max_length=255, verbose_name='Title')
    description=models.CharField(max_length=1000, default='', blank=True, verbose_name='Description')
    image=models.ImageField(null=True, blank=True,upload_to= 'images/')
    price=models.DecimalField(max_digits=5,decimal_places=2, verbose_name='Auction Price')
    listedby=models.ForeignKey(User, related_name='UserAuctionList', null=True, blank=True, on_delete=models.RESTRICT, verbose_name='Listed By')
    listedat=models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Listed At')
    isactive=models.BooleanField(default=True, verbose_name='Auction Status')
    bid=models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True, verbose_name='Bid Price')
    bidder=models.ForeignKey(User, related_name='BidWinnerList', null=True, blank=True, on_delete=models.RESTRICT, verbose_name='Bidder')
    
    def __str__(self):
        return str(self.title)
    
#User bid items
class Bid(models.Model):
    auctionid=models.ForeignKey(AuctionList, related_name='AuctionListBidList', on_delete=models.RESTRICT)
    userid=models.ForeignKey(User, related_name='UserBidList', on_delete=models.RESTRICT )
    bidprice=models.DecimalField(max_digits=5,decimal_places=2, verbose_name='Bid Price')

    def __str__(self):
        return str(self.id)
    
#User watchlist items
class WatchList(models.Model):
    userid=models.ForeignKey(User, related_name='UserWatchList', on_delete=models.RESTRICT )
    auctionid=models.ForeignKey(AuctionList, related_name='AuctionListWatchList', on_delete=models.RESTRICT)
    
    def __str__(self):
        return f"WatchList ID: {self.id}"

#User comments on auction items
class AuctionComment(models.Model):
    userid=models.ForeignKey(User, related_name='UserAuctionCommentList', on_delete=models.RESTRICT)
    auctionid=models.ForeignKey(AuctionList, related_name='AuctionListCommentList', on_delete=models.RESTRICT)
    comment=models.CharField(max_length=1000)
    postedat=models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Posted At')
    
    def __str__(self):
        return f"Comment ID: {self.id}"