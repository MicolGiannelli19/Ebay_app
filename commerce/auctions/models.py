from django.contrib.auth.models import AbstractUser
from django.db import models


# TODO: look up Abstract user Baseclass
# Find out how to edit database
class User(AbstractUser):
    image = models.URLField(
        blank=True,
        default="https://powerusers.microsoft.com/t5/image/serverpage/image-id/98171iCC9A58CAF1C9B5B9/image-size/large/is-moderation-mode/true?v=v2&px=999",
    )

    def __str__(self):
        return f"{self.username} - {self.email}"


class Listing(models.Model):
    
    CATEGORY_CHOICES = [
    ('Furniture', 'Furinture'),
    ('Clothes', 'Clothes'),
    ('Sports', 'Sports'),
    ('Toys', 'Toys'),
    ('Technology','Technology'),
    ('Pet', 'Pet'),
    ('Food', 'Food'),
    ('Other', 'Other')
    ]

    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, default='Other')
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="listings",
        blank=True,
    )
    active = models.BooleanField(default=True)
    intrested_users = models.ManyToManyField(User, blank=True, related_name="watchlist")
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    def __str__(self):
        return f"{self.title} - {self.starting_bid}"


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
