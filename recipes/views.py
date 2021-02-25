from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from foodgram.settings import PER_PAGE

from .forms import RecipeForm
from .helper import tag_collect
from .models import BR, DIN, LU, Recipe, RecipeIngredient

User = get_user_model()


def index(request):
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipes = Recipe.objects.filter(tags_filter)
    else:
        recipes = Recipe.objects.all()
    paginator = Paginator(recipes, PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "tags": tags
    }
    return render(request, "index.html", context)


def user_page(request, username):
    author = get_object_or_404(User, username=username)
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipes = Recipe.objects.filter(tags_filter).filter(
            author_id=author.id)
    else:
        recipes = Recipe.objects.filter(author_id=author.id)
    paginator = Paginator(recipes, PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "tags": tags,
        "author": author
    }
    return render(request, "user_page.html", context)


def recipe_page(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    context = {
        "recipe": recipe,
        "ingredients": ingredients,
        "author": username
    }
    return render(request, "recipe_page.html", context)


@login_required
def feed(request):
    user = request.user
    authors = User.objects.filter(
        following__subscriber=user).prefetch_related("recipes")
    paginator = Paginator(authors, PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "authors": authors,
        "page": page,
        "paginator": paginator
    }
    return render(request, "feed.html", context)


@login_required
def new_recipe(request):
    form_title = "Создание рецепта"
    btn_caption = "Создать рецепт"
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        ingredients_names = request.POST.getlist("nameIngredient")
        ingredients_values = request.POST.getlist("valueIngredient")
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        ingredict = dict(zip(ingredients_names, ingredients_values))
        for i in ingredict:
            RecipeIngredient.add_ingredient(
                RecipeIngredient,
                new_recipe.id,
                i,
                ingredict[i]
            )
        return redirect("index")

    form = RecipeForm()
    context = {
        "form_title": form_title,
        "btn_caption": btn_caption,
        "form": form
    }
    return render(request, "form_recipe.html", context)


@login_required
def edit_recipe(request, username, recipe_id):
    form_title = "Редактирование рецепта"
    btn_caption = "Сохранить"
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=username)
    recipe_redirect = redirect(
        "recipe", username=user.username, recipe_id=recipe_id)
    is_breakfast = BR
    is_lunch = LU
    is_dinner = DIN
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)

    if request.user != user:
        return recipe_redirect
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)
    if form.is_valid():
        ingredients_names = request.POST.getlist("nameIngredient")
        ingredients_values = request.POST.getlist("valueIngredient")
        form.save()
        RecipeIngredient.objects.filter(recipe_id=recipe.id).delete()
        ingredict = dict(zip(ingredients_names, ingredients_values))
        for i in ingredict:
            RecipeIngredient.add_ingredient(
                RecipeIngredient,
                recipe.id,
                i,
                ingredict[i],
            )
        return recipe_redirect

    context = {
        "form_title": form_title,
        "btn_caption": btn_caption,
        "form": form,
        "recipe": recipe,
        "is_breakfast": is_breakfast,
        "is_lunch": is_lunch,
        "is_dinner": is_dinner,
        "ingredients": ingredients
    }
    return render(request, "form_recipe.html", context)


@login_required
def favorites(request):
    user = request.user
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipes = Recipe.objects.filter(tags_filter).filter(
            favorite_recipe__user=user)
    else:
        recipes = Recipe.objects.filter(favorite_recipe__user=user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "tags": tags
    }
    return render(request, "favorites.html", context)


@login_required
def wishlist(request):
    user = request.user
    recipes = Recipe.objects.filter(wishlist_recipe__user=user)
    context = {"recipes": recipes}
    return render(request, "wishlist.html", context)
