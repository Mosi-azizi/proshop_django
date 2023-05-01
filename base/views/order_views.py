from django.shortcuts import render
from django.http import  JsonResponse
from base.serializers import ProductSerializer,UserSerializer,UserSerializerwithToken
from base.models import Order,OrderItem,Review,ShippingAddress,Product
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
#https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import  make_password
from rest_framework import status
# Create your views here.