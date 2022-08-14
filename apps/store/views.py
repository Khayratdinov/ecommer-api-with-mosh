from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
# ============================================================================ #
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# ============================================================================ #
from ..users.models import Customer
from .models import CartItem, Collection, Product, OrderItem, Review, Cart, Order
from .serializers import (CartItemSerializer, CollectionSerializer, ProductSerializer, 
                          ReviewSerializer, CartSerializer, AddCartItemSerializer, 
                          UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer,
                          UpdateOrderSerializer)
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsADminOrReadOnly




# ============================== PRODUCTVIEWSET ============================== #

class ProductViewSet(ModelViewSet):


    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    permission_classes = [IsADminOrReadOnly]
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {'request': self.request}


    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'})

        return super().destroy(request, *args, **kwargs) 



# ============================= COLLECTIONVIEWSET ============================ #


class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsADminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'})
        return super().destroy(request, *args, **kwargs) 




# =============================== REVIEWVIEWSET ============================== #

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}




# ================================ CARTVIEWSET =============================== #

class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin,
                  GenericViewSet):

    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer



# ============================== CARTITEMVIEWSET ============================= #


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
   
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
                .filter(cart_id=self.kwargs['cart_pk']) \
                .select_related('product')




# =============================== ORDER VIEWSET ============================== #

class OrderViewSet(ModelViewSet):
    
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)






