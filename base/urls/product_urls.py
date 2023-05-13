from django.urls import path
from base.views import product_views


urlpatterns = [
    path('',product_views.getProducts, name="base"),

    path('create/', product_views.createProduct, name='crate-product'),
    path('upload/', product_views.uploadImage, name='image-upload'),

    path('<str:pk>/',product_views.getProduct, name="product"),
    path('<str:pk>/reviews/', product_views.createProductReview, name="create-review "),

    path('delete/<str:pk>/',product_views.deleteProduct, name="delete-product"),
    path('update/<str:pk>', product_views.updateProduct, name='update-product'),


]
