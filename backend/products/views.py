from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Product,Category,Order,CartItem,Cart,OrderItem
from .serializers import ProductSerializer,CategorySerializer,CartSerializer,OrderSerializer,OrderItemSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # partial=True for partial updates
        serializer.is_valid(raise_exception=True)        

        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # partial=True for partial updates
        serializer.is_valid(raise_exception=True)        

        return Response(serializer.data)\
        
    def get_queryset(self):
        # Get the category name from query parameters
        category_name = self.request.query_params.get('name')
        if category_name:
            return Product.objects.filter(category__name=category_name)
        return Category.objects.all()  # Optionally return all products if no category is specified
    
class ProductsByCategoryView(APIView):
    def get(self, request, category_name):
        products = Product.objects.filter(category__name=category_name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def add_to_cart(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        cart_item.quantity += 1
        cart_item.save()
        return Response({'status': 'Product added to cart'})
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the order
        serializer.save(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def create_order(self, request):
#         cart = Cart.objects.get(user=request.user)
#         total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
#         order = Order.objects.create(user=request.user, total_price=total_price)
#         order.products.set(cart.products.all())
#         cart.products.clear()  # Clear cart after placing order
#         return Response({'status': 'Order created', 'order_id': order.id})