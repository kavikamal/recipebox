"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from recipebox.views import home_view, author_view, recipe_view, new_recipe_add, login_user, signup_user, logout_user
from recipebox.views import signup_user, home_view, new_recipe_add, logout_user, login_user, author_view, recipe_view, edit_recipe, favorite_recipe
from recipebox.models import Author, Recipe

admin.site.register(Author)
admin.site.register(Recipe)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='homepage'),
    path('recipe/<int:recipe_id>', recipe_view),
    path('author/<int:author_id>', author_view),
    path('newrecipeadd/', new_recipe_add),
    path('login/', login_user),
    path('signup/', signup_user),
    path('logout/', logout_user),
    path('edit_recipe/<int:recipe_id>', edit_recipe.as_view()),
    path('favorite/<int:id>/', favorite_recipe),
]
