from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(
        'Recipe', related_name='favorites', symmetrical=False, blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,)
    description = models.CharField(max_length=300)
    time = models.IntegerField(default=0)
    instructions = models.TextField(max_length=5000)

    def get_absolute_url(self):
        return reverse('recipe_edit', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
