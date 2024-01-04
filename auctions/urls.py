from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuctionList_ListView.as_view(), name="index"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.user_registration, name="register"),
    path("category/<int:categoryid>", views.AuctionListByCategory_ListView.as_view(), name="categorydetailpage"),
    path("category/", views.Category_Listview.as_view(), name="category"),
    path("watchlist/<int:auctionid>", views.delete_watchlist, name="deletewatchlist"),
    path("watchlist", views.AuctionList_Watchlist_ListView.as_view(), name="watchlist"),
    path("createlisting", views.create_auction_listing, name="createlisting"),
    path("detailpage/<int:auctionid>", views.detail_page, name="detailpage"),
    

]
