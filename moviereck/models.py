from django.db import models

# Create your models here.

class Category(models.Model):

    MOVIE_CATEGORY = [
        ('comady', 'Comady'),
        ('action', 'Action'),
        ('thriller', 'Thiller'),
        ('drama', 'Drama'),
        ('romantic', 'Romantic'),
        ('horror', 'Horror'),
        ('sci-fi', 'Sci-fi'),
        ('crime', 'Crime'),

    ]
    category_name = models.CharField(max_length=255, choices=MOVIE_CATEGORY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name



class Movie(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField()
    description = models.TextField(blank=True)
    release = models.DateField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
