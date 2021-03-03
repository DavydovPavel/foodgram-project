import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from recipes.models import Ingredient, Recipe, RecipeIngredient
from users.models import Favorite, Follow, Wishlist

SUCCESS_RESPONSE = JsonResponse({"success": True})
FAIL_RESPONSE = HttpResponse()


@require_http_methods(["POST"])
def add_favorite(request):
    body = json.loads(request.body)
    recipe_id = body.get("id")
    if recipe_id is not None:
        _, created = Favorite.objects.get_or_create(
            user_id=request.user.id, recipe_id=recipe_id)
        if created:
            return SUCCESS_RESPONSE
        return FAIL_RESPONSE
    return FAIL_RESPONSE


@require_http_methods(["DELETE"])
def remove_favorite(request, recipe_id):
    deleted = Favorite.objects.filter(
        user_id=request.user.id, recipe_id=recipe_id).delete()
    return SUCCESS_RESPONSE if deleted else FAIL_RESPONSE


@require_http_methods(["POST"])
def add_wishlist(request):
    body = json.loads(request.body)
    recipe_id = body.get("id")
    if recipe_id is not None:
        _, created = Wishlist.objects.get_or_create(
            user_id=request.user.id, recipe_id=recipe_id)
        if created:
            return SUCCESS_RESPONSE
        return FAIL_RESPONSE
    return FAIL_RESPONSE


@require_http_methods(["DELETE"])
def remove_wishlist(request, recipe_id):
    deleted = Wishlist.objects.filter(
        user_id=request.user.id, recipe_id=recipe_id).delete()
    return SUCCESS_RESPONSE if deleted else FAIL_RESPONSE


@require_http_methods(["POST"])
def add_subscription(request):
    body = json.loads(request.body)
    following_id = body.get("id")
    user = request.user
    if user.id != following_id and following_id is not None:
        _, created = Follow.objects.get_or_create(
            subscriber_id=user.id, following_id=following_id)
        if created:
            return SUCCESS_RESPONSE
        return FAIL_RESPONSE
    return FAIL_RESPONSE


@require_http_methods(["DELETE"])
def remove_subscription(request, following_id):
    user = request.user
    deleted = Follow.objects.filter(
        subscriber_id=user.id, following_id=following_id).delete()
    return SUCCESS_RESPONSE if deleted else FAIL_RESPONSE


def remove_recipe(request, username, recipe_id):
    if request.user.username == username:
        Recipe.objects.filter(id=recipe_id).delete()
        return redirect("user", username)
    return redirect("recipe", username, recipe_id)


@require_http_methods(["GET"])
def get_ingredients(request):
    query = request.GET.get("query").lower()
    ingredients = Ingredient.objects.filter(
        title__contains=query).values("title", "dimension")
    return JsonResponse(list(ingredients), safe=False)


def get_wishlist(request):
    user = request.user
    wishlist_filter = Wishlist.objects.filter(
        user_id=user.id).values_list("recipe", flat=True)
    ingredient_filter = RecipeIngredient.objects.filter(
        recipe_id__in=wishlist_filter).order_by("ingredient")
    ingredients = {}
    for ingredient in ingredient_filter:
        if ingredient.ingredient in ingredients:
            ingredients[ingredient.ingredient] += ingredient.amount
        else:
            ingredients[ingredient.ingredient] = ingredient.amount

    wishlist = []
    for k, v in ingredients.items():
        wishlist.append(f"{k.title} - {v} {k.dimension} \n")
    wishlist.append("\n\n\n\n")

    response = HttpResponse(wishlist, content_type='application/txt')
    # "Content-Type: text/plain")
    response["Content-Disposition"] = 'attachment; filename="wishlist.txt"'
    return response
