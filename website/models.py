from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField
category_array = [("Bars", "Bars"), ("Shaving", "Shaving"), ("Oil", "Oil"), ("Shampoo", "Shampoo"), ("Salts","Salts"), ("Cream", "Cream"), ("Liquid soap", "Liquid soap"), ("Clear soap", "Clear soap"), ("Cologne & Perfume", "Cologne & Perfume"), ("Lotion", "Lotion")]
# Create your models here.
class userAccount(models.Model):
    street_address = models.CharField(max_length=150, default="")
    apartment = models.CharField(max_length=150, default="")
    city = models.CharField(max_length=150, default="")
    Province = models.CharField(max_length=150, default="")
    Country = models.CharField(max_length=150, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.user.username

class product(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.IntegerField()
    category = models.CharField(max_length=150, choices=category_array, default="")
    ig = CloudinaryField('image')
    description = models.TextField(default="")
    featured = models.BooleanField(default=False)
    palm_free = models.BooleanField(default=False)
    plastic_free = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return self.name

def create_user_account(sender, **Kwargs):
    if Kwargs["created"]:
        new_user = userAccount.objects.create(user=Kwargs["instance"])

post_save.connect(create_user_account, sender=User)

## order model
class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=False)
    products = models.TextField(default="", blank=False)
    complete = models.BooleanField(default=False)
    shipping = models.BooleanField(default=False)
    total = models.CharField(default="",blank=False,max_length=250)
    objects = models.Manager()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Order no: " + str(self.id) + " by "   + self.user.first_name + " placed on " + str(self.date)