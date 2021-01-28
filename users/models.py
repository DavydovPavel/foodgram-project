from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Follow(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriber")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["subscriber", "following"],
                                    name="follow_uniq")
        ]


class Favorites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_subscriber")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipe")


class Wishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlist_subscriber")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="wishlist_recipe")
