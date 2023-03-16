from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.db import models
from tabnanny import verbose
from tkinter import CASCADE
from django.core.validators import MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    pass

class Category (MPTTModel):
    name = models.CharField(max_length=150, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name} | в каталозі: {self.parent}' if self.parent else self.name

class Auction(models.Model):
    nameStuff = models.CharField(max_length=200)
    descriptionStuff = models.TextField(max_length=1000)
    initialPrice = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="auctions")
    imageStuff = models.ImageField(upload_to="img/")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watch_list")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    active = models.BooleanField(default=True)
    openDatetime = models.DateTimeField(auto_now_add=True)
    closeDatetime = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_winner")
   
class Bet(models.Model):
    userName = models.ForeignKey(User, on_delete=models.CASCADE)
    stuff = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bet')
    stuffBet = models.DecimalField(max_digits=12, decimal_places=2, null=True)

class Comment(models.Model):
    userName = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    stuff = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction")
    commentText = models.TextField(max_length=400)
    dateandtime = models.DateTimeField(auto_now_add=True)