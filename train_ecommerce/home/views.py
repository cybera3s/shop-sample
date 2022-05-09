from django.shortcuts import render, get_object_or_404
from orders.forms import *
from .models import *
from django.views import View
from .tasks import all_bucket_objects_task


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, 'home/detail.html', {'product': product, 'form': form})

    def post(self, request):
        ...


class BucketHome(View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = all_bucket_objects_task()

        return render(request, self.template_name, {'objects': objects})


# class DeleteBucket(view):
#     def get(self, request, obj_name):
#         delete_bucket_object_task(obj_name)
#         return redirect('home:bucket')