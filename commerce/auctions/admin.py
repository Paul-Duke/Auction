from django.contrib import admin
from .models import Auction, Bet, Comment, Category, User

# Register your models here.
admin.site.register(Auction)
admin.site.register(Bet)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User)