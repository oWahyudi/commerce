from django import forms
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils import timezone
import pytz
from .models import User,Category,AuctionList,WatchList,Bid,AuctionComment
from .views import get_paginate_by,get_datetime_formatting

#Customize datetime formatting and rename field display.
def datetime_field_display(field_name,short_description,formatting):
    def rename_method(self,obj):
        value = getattr(obj, field_name, None)  
        # Convert the UTC datetime to the 'Asia/Singapore' timezone
        singapore_timezone=pytz.timezone('Asia/Singapore')
        local_created=timezone.localtime(value,singapore_timezone)
        return local_created.strftime(formatting) if value else None
    
    rename_method.short_description=short_description
    return rename_method


# Common function to rename field name display 
def rename_field_display(field_name,short_description):
    def rename_method(self,obj):
        return getattr(obj, field_name, None)
    
    rename_method.short_description=short_description
    return rename_method
                       

# ModelAdmin

class CustomLogEntryAdmin(admin.ModelAdmin):
    list_display = ('formatted_action_time', 'user', 'action_flag','content_type','object_repr')
    formatted_action_time=datetime_field_display('action_time','Date/Time',get_datetime_formatting())


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','email','is_active')  
    list_display_links = ('username',) 
    search_fields = ['username','first_name','last_name','email'] 
    readonly_fields = ('password','date_joined','username','last_login') 


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    list_display_links = ('name',) 
    search_fields = ['name'] 

class AuctionListAdminForm(forms.ModelForm):
    class Meta:
        model=AuctionList
        fields = '__all__'
        widgets={
            'description':forms.Textarea(),

        }

class AuctionListAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','price','bid','bidder','categoryid','isactive','listedby','formatted_listedat')  
    list_display_links = ('title',) 
    #listedby__username -> Retrieve the username associated with the foreign key field listedby
    search_fields = ['title','description','price','categoryid__name','listedby__username'] 
    readonly_fields = ('id','bid','bidder') 
    formatted_listedat=datetime_field_display('listedat','Listed At',get_datetime_formatting())
    form=AuctionListAdminForm



class WatchListAdmin(admin.ModelAdmin):
    list_display = ('id','rename_userid', 'rename_auctionid')  
    list_display_links = ('id','rename_userid') 
    search_fields = ['userid__username','auctionid__title'] 
    readonly_fields = ('id',) 
    rename_userid=rename_field_display('userid','Username')
    rename_auctionid=rename_field_display('auctionid','Auction Title')


class BidAdmin(admin.ModelAdmin):
    list_display = ('id','userid', 'auctionid','bidprice')  
    list_display_links = ('userid',) 
    search_fields = ['userid'] 
    readonly_fields = ('id','userid','auctionid') 


class AuctionCommentAdminForm(forms.ModelForm):
    class Meta:
        model=AuctionComment
        fields='__all__'
        widgets={
            'comment':forms.Textarea(),
        }

class AuctionCommentAdmin(admin.ModelAdmin):
    list_display = ('userid', 'auctionid','comment','postedat')  
    list_display_links = ('userid',) 
    search_fields = ['userid','comment'] 
    readonly_fields = ('id','postedat','auctionid','userid') 
    form=AuctionCommentAdminForm



# Register your models here.

App_Auction_Admin=[(LogEntry,CustomLogEntryAdmin), 
                   (User, UserAdmin), 
                   (Category, CategoryAdmin), 
                   (AuctionList, AuctionListAdmin), 
                   (WatchList, WatchListAdmin), 
                   (Bid, BidAdmin), 
                   (AuctionComment, AuctionCommentAdmin)
                ]
    
    
for model, modeladmin in App_Auction_Admin:
    admin.site.register(model, modeladmin)



