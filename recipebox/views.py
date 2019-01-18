from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from django.shortcuts import reverse
from recipebox.models import Recipe, Author
from recipebox.forms import NewRecipeAddForm, LoginForm, SignupForm


def home_view(request):
    recipe_list = Recipe.objects.all()
    return render(request, 'home_view.html', {'recipe_list': recipe_list})


def recipe_view(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'recipe_view.html', {'data': recipe})


def author_view(request, author_id):
    name = Author.objects.get(pk=author_id).name
    recipes_object = Recipe.objects.filter(author__name=name)
    favorites = Author.objects.get(pk=author_id).favorites.all()
    recipes = []
    for recipe in recipes_object:
        recipes.append(recipe)
    author = {
        'name': name,
        'recipes': recipes,
        'favorites': favorites
    }
    return render(request, 'author_view.html', author)


def author_view(request, author_id):

    data = {
        'author': Author.objects.get(pk=author_id),
        'recipes': list(Recipe.objects.all().filter(
            author_id=author_id).values()
        )
    }
    return render(request, 'author_view.html', {'data': data})


@login_required
def new_recipe_add(request):
    form = None
    if request.method == "POST":
        print(request)
        form = NewRecipeAddForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=Author.objects.filter(id=data['author']).first(),
                description=data['description'],
                time=data['time'],
                instructions=data['instructions'],
            )
            return render(request, 'success_view.html')
    else:
        print("new_recipe_add else")
        form = NewRecipeAddForm()
    return render(request, 'new_recipe_add.html', {'form': form})


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = 'edit_recipe.html'
    fields = ['title', 'description', 'time', 'instructions']

    def get_success_url(self):
        recipeid = self.kwargs['pk']
        return reverse('recipe_edit', kwargs={'pk': recipeid})


def favorite_recipe(request, id):
    recipe = Recipe.objects.filter(id=id).first()
    author = Author.objects.get(pk=recipe.author_id)
    if recipe in author.favorites.all():
        author.favorites.remove(recipe)
    else:
        author.favorites.add(recipe)
    recipes = author.favorites.all()
    print(recipes)
    return render(request, 'favorite_recipe.html', {'recipe': recipe, 'recipes': recipes})


def signup_user(request):
    form = SignupForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password']
        )
        Author.objects.create(
            name=data['name'],
            bio=data['bio'],
            user=user
        )
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'signup.html', {'form': form})


def login_user(request):
    next_page = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user is not None:
                login(request, user)
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(reverse('homepage'))
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'next': next_page})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
