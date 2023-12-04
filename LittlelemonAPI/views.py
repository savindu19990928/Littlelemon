from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Category, Order, Booking
from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, UserSerilializer, BookingSerializer
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from rest_framework import viewsets
from rest_framework import status

class BookingView(viewsets.ViewSet):
    def list(self, request):
        bookings = Booking.objects.all()
        items = BookingSerializer(bookings, many=True)
        return Response(items.data)
    
    def create(self, request):
        # Deserialize the request data using the serializer
        serializer = BookingSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Save the validated data to the Booking model
            serializer.save()

            # Return a success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return a validation error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['category__title']
    ordering_fields = ['price', 'inventory']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

# class CartView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Cart.objects.all().filter(user=self.request.user)

#     def delete(self, request, *args, **kwargs):
#         Cart.objects.all().filter(user=self.request.user).delete()
#         return Response("ok")


# class OrderView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
    
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return Order.objects.all()
#         elif self.request.user.groups.count()==0: #normal customer - no group
#             return Order.objects.all().filter(user=self.request.user)
#         elif self.request.user.groups.filter(name='Delivery Crew').exists(): #delivery crew
#             return Order.objects.all().filter(delivery_crew=self.request.user)  #only show oreders assigned to him
#         else: #delivery crew or manager
#             return Order.objects.all()

    # def create(self, request, *args, **kwargs):
    #     menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
    #     if menuitem_count == 0:
    #         return Response({"message:": "no item in cart"})

    #     data = request.data.copy()
    #     total = self.get_total_price(self.request.user)
    #     data['total'] = total
    #     data['user'] = self.request.user.id
    #     order_serializer = OrderSerializer(data=data)
    #     if (order_serializer.is_valid()):
    #         order = order_serializer.save()

    #         items = Cart.objects.all().filter(user=self.request.user).all()

    #         for item in items.values():
    #             orderitem = OrderItem(
    #                 order=order,
    #                 menuitem_id=item['menuitem_id'],
    #                 price=item['price'],
    #                 quantity=item['quantity'],
    #             )
    #             orderitem.save()

    #         Cart.objects.all().filter(user=self.request.user).delete() #Delete cart items

    #         result = order_serializer.data.copy()
    #         result['total'] = total
    #         return Response(order_serializer.data)
    
    # def get_total_price(self, user):
    #     total = 0
    #     items = Cart.objects.all().filter(user=user).all()
    #     for item in items.values():
    #         total += item['price']
    #     return total


class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0: # Normal user, not belonging to any group = Customer
            return Response('Not Ok')
        else: #everyone else - Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)



class GroupViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerilializer(data=request.data)
        
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DeliveryCrewViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     def list(self, request):
#         users = User.objects.all().filter(groups__name='Delivery Crew')
#         items = UserSerilializer(users, many=True)
#         return Response(items.data)

#     def create(self, request):
#         #only for super admin and managers
#         if self.request.user.is_superuser == False:
#             if self.request.user.groups.filter(name='Manager').exists() == False:
#                 return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        
#         user = get_object_or_404(User, username=request.data['username'])
#         dc = Group.objects.get(name="Delivery Crew")
#         dc.user_set.add(user)
#         return Response({"message": "user added to the delivery crew group"}, 200)

#     def destroy(self, request):
#         #only for super admin and managers
#         if self.request.user.is_superuser == False:
#             if self.request.user.groups.filter(name='Manager').exists() == False:
#                 return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
#         user = get_object_or_404(User, username=request.data['username'])
#         dc = Group.objects.get(name="Delivery Crew")
#         dc.user_set.remove(user)
#         return Response({"message": "user removed from the delivery crew group"}, 200)