from django.urls import path
from . import views


urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('',views.getRoutes, name="routes"),
    path('products/',views.getProducts, name="base"),
    path('users/profile/',views.getUserProfile, name='user-profile'),
    path('users/',views.getUsers, name='users'),

    path('product/<str:pk>/',views.getProduct, name="product"),

]
