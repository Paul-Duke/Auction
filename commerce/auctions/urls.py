from unicodedata import category
from django.urls import path


from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("categories/<str:category>/<int:auction_id>", views.auction, name="auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category>/<int:auction_id>/to_watchlist", views.to_watchlist, name="to_watchlist"),
    path("categories/<str:category>/<int:auction_id>/del_from_watchlist", views.del_from_watchlist, name="del_from_watchlist"),
    path("create_auction", views.create_auction, name="create_auction"),
    path("categories/<str:category>/<int:auction_id>/bet", views.bet, name="bet"),
    path("categories/<str:category>/<int:auction_id>/comment", views.comment, name="comment"),
    path("categories/<str:category>/<int:auction_id>/close", views.close, name="close"),
    path("auctions_history", views.auctions_history, name="auctions_history"),
    path("achievements", views.achievements, name="achievements")
] 