
from django.urls import path, include
from .views import *

app_name = 'home'

bucket_urls = [
    path('', BucketHome.as_view(), name='bucket'),
    path('delete_obj_bucket/<key>', DeleteBucketObject.as_view(), name='delete_obj_bucket'),
]


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('bucket/', include(bucket_urls)),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>', HomeView.as_view(), name='category_filter'),
]
