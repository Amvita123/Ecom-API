from rest_framework.permissions import IsAuthenticated
from accounts.permissions import AdminORSeller
from django.db.models import Q
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User, Product, Order, Address
from .serializers import ProductSerializer, OrderSerializer


class ProductProfileView(APIView):
    permission_classes = [IsAuthenticated, AdminORSeller]

    def get(self, request, pk=None):
        products = Product.objects.filter(owner=request.user)
        created_at = request.GET.get('created_at', None)
        if created_at:
            try:
                created_at_date = datetime.strptime(created_at, '%Y-%m-%d')
                products = products.filter(created_at__gte=created_at_date)
            except ValueError:
                return Response({"message": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        search_query = request.GET.get('search', None)
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(stock_quality__icontains=search_query)
            )
        products = products.order_by('-created_at')[::]
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "This Products Is Not Available."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            product.owner = request.user
            product.save()
            return Response(
                {"message": "Product added successfully", "product": ProductSerializer(product).data}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)
        if product.owner != request.user:
            return Response({"message": "You do not have permission to update this product"},status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Product updated successfully", "product": serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)
        if product.owner != request.user:
            return Response({"message": "You do not have permission to delete this product"}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.GET.get('search', None)
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        address = request.data.get('address')
        status = request.data.get('status')

        try:
            address = Address.objects.filter(user=request.user).first()
        except Address.DoesNotExist:
            return Response({"message": "No address found for this user"}, status=status.HTTP_400_BAD_REQUEST)
        if not address:
            return Response({"message": "User does not have an address"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "no product match"}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(
            user=request.user,
            product = product,
            quantity = quantity,
            address=address,
            status = status,
        )
        serializer = OrderSerializer(order)
        return Response({"message": "order create successful", "order": serializer.data}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        status_value = request.data.get('status')
        if status_value is None:
            return Response({"message": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)
        if status_value not in ['pending', 'shipped', 'delivered', 'cancelled']:
            return Response({"message": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status_value
        order.save()
        serializer = OrderSerializer(order)
        return Response({"message": "Order status updated", "order": serializer.data}, status=status.HTTP_200_OK)

