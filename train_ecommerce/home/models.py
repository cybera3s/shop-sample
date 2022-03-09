from django.db import models
from django.urls import reverse


class Product(models.Model):
    category = models.ManyToManyField('Category', related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/5m/%d/')
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug])

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
