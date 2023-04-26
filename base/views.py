from django.shortcuts import render
from django.http import  JsonResponse
from .serializers import ProductSerializer,UserSerializer,UserSerializerwithToken
from .models import Order,OrderItem,Review,ShippingAddress,Product
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
#https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    #https://github.com/jazzband/djangorestframework-simplejwt/blob/master/rest_framework_simplejwt/serializers.py
    def validate(self, attrs):
        data = super().validate(attrs)

        #data['username'] = self.user.username
        #data['email'] = self.user.email
        serializer = UserSerializerwithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/base/',
        '/api/base/create/',

        '/api/base/upload/',

        '/api/base/<id>/reviews/'
        
        '/api/base/top/',

        '/api/base/<id>/',

        '/api/base/delete/<id>/',
        '/api/base/<update>/<id>/',

    ]
    return Response(routes)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = User.objects.all()
    serializers = UserSerializer(users, many=True)
    return Response(serializers.data)



@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)