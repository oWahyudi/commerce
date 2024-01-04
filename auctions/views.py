from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.conf import settings

from .forms import User,CreateListingForm,BidForm,UserRegistrationForm
from .models import AuctionList,WatchList,Bid,AuctionComment,Category   

#Common function for retrieving the default paginate setting.
def get_paginate_by():
    return getattr(settings,'DEFAULT_APPS_AUCTION_PAGINATE_BY',1)

#Common function for retrieving the default datetime format setting.
def get_datetime_formatting():
    return getattr(settings,'DEFAULT_APPS_AUCTION_DATETIME_FORMATTING',None)

def get_fileserver_url():
    return getattr(settings,'DEFAULT_FILE_SERVER_URL',None)

def set_fileserver_url_context(context):
    context['FILE_SERVER_URL'] = get_fileserver_url()
    return context



get_fileserver_url


class AuctionList_ListView(ListView):
    model=AuctionList
    template_name='auctions/index.html'
    paginate_by=get_paginate_by()

    def get_queryset(self):
        auctionlist=AuctionList.objects.all().order_by('-listedat')
        return auctionlist
    
    # Specify the path for the file server URL.
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        new_context=set_fileserver_url_context(context)
        return context
    
    

class AuctionListByCategory_ListView(ListView):
    model=AuctionList
    template_name='auctions/index.html'
    paginate_by=get_paginate_by()

    def get_queryset(self):
        categoryid = self.kwargs.get('categoryid')
        auctionlist=AuctionList.objects.filter(categoryid=categoryid).order_by('-listedat')
        return auctionlist 
    
    # Specify the path for the file server URL.
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        new_context=set_fileserver_url_context(context)
        return new_context


class AuctionList_Watchlist_ListView(ListView):
    model=AuctionList
    template_name='auctions/watchlist.html'
    paginate_by=get_paginate_by()

    def get_queryset(self):
        user=self.request.user
        # Retrieve the list of auction IDs through the related name "UserWatchList" on the WatchList model.
        watchlist_auctionid_queryset = user.UserWatchList.values_list('auctionid', flat=True)

        # Filter AuctionList based on the id values
        auctionlist =AuctionList.objects.filter(id__in=watchlist_auctionid_queryset).order_by('-listedat')
        return auctionlist
    

    # Specify the path for the file server URL.
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        new_context=set_fileserver_url_context(context)
        return context


class Category_Listview(ListView):
    model=Category
    template_name='auctions/categorylisting.html'
    paginate_by=get_paginate_by()

    def get_queryset(self):
        categorieslist=Category.objects.all().order_by('name')
        return categorieslist



def get_current_user(request):
    user=None
    if request.user.is_authenticated:
        user=request.user
    return user
    

def get_watchlist_count(user):
    watchlist_count=WatchList.objects.filter(userid=user).count()
    return watchlist_count


def set_watchlist_count_in_session(request):
    user=get_current_user(request)
    watchlist_count = get_watchlist_count(user)
    request.session['watchlistcount'] = watchlist_count


def login_user(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            set_watchlist_count_in_session(request)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "messagetype": "error"
            })
    else:
        return render(request, "auctions/login.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def create_user(request,firstname,lastname,username,email,password):
    try:
        user = User.objects.create_user(username, email, password)
        user.first_name=firstname
        user.last_name=lastname
        user.save()
    except IntegrityError:
        context={"message": "Username already taken.",
                 "messagetype": "error"
                }
        return render(request, "auctions/register.html", context)
    
    return user


def user_registration(request):
    form=UserRegistrationForm()
    context={'form':form}
    
    if request.method == "POST":
        form=UserRegistrationForm(request.POST)
        context['form']=form

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]


  

        if form.is_valid():
            if not password or not confirmation  or password != confirmation:
                form.add_error(None, "Please enter both a password and its confirmation.")
                context['form']=form
                return render(request, "auctions/register.html",context)
            
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']

            #Attempt to create a user
            user=create_user(request,first_name,last_name,username,email,password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))


    return render(request, "auctions/register.html",context)

    
def delete_watchlist(request, auctionid):
    try:
        user=request.user
        watchlist=WatchList.objects.filter(auctionid=auctionid,userid=user)
        if watchlist:
            watchlist.delete()
            set_watchlist_count_in_session(request)
    except WatchList.DoesNotExist:
        watchlist=None
    return redirect(reverse('watchlist'))



def save_auction_listing(user,form):
    instance=form.save(commit=False)
    instance.listedby=user
    instance.save()


def set_close_auction(auction):
    auction=AuctionList.objects.filter(pk=auction.pk).first()
    
    if auction:
        auction.isactive=False
        auction.save()

    return auction


def create_auction_listing(request):
    form=CreateListingForm(label_suffix="") # Default form instance
    context ={'form': form}

    set_watchlist_count_in_session(request)
    
    if request.method == "POST":
        form=CreateListingForm(request.POST,request.FILES,label_suffix="")
        context['form']=form

        if form.is_valid():
            save_auction_listing(request.user,form)
            return redirect(reverse('index'))
  
    return render(request, "auctions/createlisting.html",context)


def get_auctionlist(auctionid):
    auction=AuctionList.objects.filter(id=auctionid).first()
    return auction


def get_watchlist(user,auction):
    watchlist=WatchList.objects.filter(userid=user,auctionid=auction).first()
    return watchlist
    

def save_watchlist(user,auction):
    watchlists_exist=WatchList.objects.filter(userid=user,auctionid=auction).exists()
    if not watchlists_exist:
        watchlist=WatchList(userid=user,auctionid=auction)
        watchlist.save()


def save_comments(user,auction,comment):
    comment=AuctionComment(userid=user,auctionid=auction,comment=comment)
    comment.save()


def get_comments_list(user,auction):
    comments=AuctionComment.objects.filter(userid=user,auctionid=auction).order_by('-postedat')
    return comments


def get_bid_count(auction):
    bid_count=Bid.objects.filter(auctionid=auction).count()
    return bid_count


def save_bid(user,auction,form):
    instance=form.save(commit=False)
    instance.auctionid=auction
    instance.userid=user
    instance.save()


def update_auctionlist(user,auction,bidprice):
    auction.bid=bidprice
    auction.bidder=user
    auction.save()


def detail_page(request,auctionid):
    form=BidForm()
    context = {'form' : form}
    user=get_current_user(request)
 
    #Get auction details
    auction=get_auctionlist(auctionid)
    context['auction']=auction

    #Get watchlist details
    watchlist=get_watchlist(user,auction)
    context['watchlist']=watchlist

    #Get bid count
    bid_count=get_bid_count(auction)
    context['bidcount']=bid_count

    #Get comment list
    commentlist=get_comments_list(user,auction)
    context['commentlist']=commentlist

    
    if not auction:
        form.page_message_error='Auction not found'
        context['form']=form


    if auction and request.method == "POST":
        existing_bidprice= auction.bid or auction.price
        form=BidForm(request.POST,existing_bidprice=existing_bidprice) 
        context['form']=form
        
        actiontask = request.POST["actiontask"]
        
        if actiontask == "watchlist":
            form.errors.clear()
            context['form']=form
            save_watchlist(user,auction)
            set_watchlist_count_in_session(request)
            url = reverse('detailpage', args=[auctionid])
            return redirect(url) 
       
        if actiontask == "closeauction":
            form.errors.clear()
            context['form']=form
            new_auction=set_close_auction(auction)
            
            #Update successful
            if new_auction:
                url = reverse('detailpage', args=[auctionid])
                return redirect(url) 
        
        if actiontask == "postcomment":
            form.errors.clear()
            context['form']=form
            new_comment = request.POST["comments"]
            save_comments(request.user,auction,new_comment)
            commentlist=get_comments_list(user,auction)
            context['commentlist']=commentlist

            url = reverse('detailpage', args=[auctionid])
            return redirect(url) 

            
        
        #Place Bid
        if form.is_valid():
            try:
                with transaction.atomic():
                    bidprice=form.cleaned_data['bidprice']
                    save_bid(user,auction,form)          
                    update_auctionlist(user,auction,bidprice)
                
                return redirect(reverse('index'))
            
            except Exception as e:
                form.add_error(None, "Sorry, we couldn't process your request at the moment. Please try again later")
                context['form']=form
             
    return render(request, 'auctions/detailpage.html', context)
