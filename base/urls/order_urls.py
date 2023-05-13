from django.urls import path
from base.views import order_views as view

urlpatterns = [
    path('',view.getOrder,name='orders'),
    path('add/',view.addOrderItems, name='orders-add'),
    path('myorders/',view.getMyOrder, name='myorders'),

    path('<str:pk>/deliver/',view.updateOrderToDelivered, name='order-deliverd'),
    path('<str:pk>/',view.getOrderById, name='user-order'),
    path('<str:pk>/pay/',view.updateOrderToPaid, name='pay'),

]