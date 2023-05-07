from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from base.serializers import UserSerializer,UserSerializerwithToken

#https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import  make_password
from rest_framework import status



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

@api_view(['POST'])
#@permission_classes([IsAdminUser])
def registerUser(request):
    data = request.data
    try:
     user = User.objects.create_user(
          first_name = data['name'],
          username= data['email'],
          email = data['email'],
          password= make_password(data['password'])
      )
    except:
        message = {'detail':'User with this email already exists'}
        return  Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializerwithToken(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerwithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username =data['email']
    user.email = data['email']
    print(user.email,user.username)
    if data['password'] !='':
        user.password = make_password(data['password'])
    user.save()
    return  Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializers = UserSerializer(users, many=True)
    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was Deleted')