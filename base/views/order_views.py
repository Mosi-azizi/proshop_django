from django.shortcuts import render

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Order,OrderItem,ShippingAddress,Product
from base.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer

from rest_framework import status
from datetime import datetime




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0 :
        message = {'detail':'No Order Items'}
        return Response(message, status = status.HTTP_400_BAD_REQUEST)
    else:

        #(1) Create order
        order = Order.objects.create(
            user = user,
            paymentMethod= data['paymentMethod'],
            taxPrice= data['taxPrice'],
            shippingPrice= data['shippingPrice'],
            totalPrice= data['totalPrice']
        )
        #(2) Create shipping address
        shipping = ShippingAddress.objects.create(
            order = order,
            address= data['shippingAddress']['address'],
            city= data['shippingAddress']['city'],
            postalCode= data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country']
        )
        #(3) Create order items and set order to ordeItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])
            item = OrderItem.objects.create(
                product = product,
                order= order,
                name = product.name,
                qty=i['qty'],
                price = i['price'],
                image = product.image.url,

            )
             #(4) update stock
            product.countInStock -= item.qty
            product.save()

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getOrderItems(request):
    orderItems = OrderItem.objects.all()
    serializer = OrderItemSerializer(orderItems, many=True)
    return  Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrder(requset):
    user = requset.user
    order = user.order_set.all()
    serizliser = OrderSerializer(order, many=True)
    return Response(serizliser.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user

    try:
       order = Order.objects.get(_id=pk)
       if user.is_staff or order.user == user:
           serializer = OrderSerializer(order, many=False)
           return Response(serializer.data)
       else:
            message = {'Detail':'Not authorized to view this order'}
            Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'derail':'Order does not exitst '}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return  Response('Order was paid')