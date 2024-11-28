from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime
from accounts.models import Product, Order, Address
from .serializers import ProductSerializer, OrderSerializer


class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
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
        products = products.order_by('-created_at')
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        if not orders.exists():
            return Response({"message": "You Have No Order"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        street_address = request.data.get('street_address')
        city = request.data.get('city')
        state = request.data.get('state')
        pincode = request.data.get('pincode')
        country = request.data.get('country')
        is_default = request.data.get('is_default', False)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"message": "Quantity Must Be Valid Number"}, status=status.HTTP_400_BAD_REQUEST)

        if quantity <=0:
            return Response({"message": "Quantity Always Grater Then Zero"}, status=status.HTTP_400_BAD_REQUEST)

        if not all([street_address, city, state, pincode, country]):
            return Response({"message": "Please enter street_address, city, state, pincode, country"},
                            status=status.HTTP_400_BAD_REQUEST)
        street_address = street_address.strip().lower()
        city = city.strip().lower()
        state = state.strip().lower()
        pincode = pincode.strip()
        country = country.strip().lower()
        existing_address = Address.objects.filter(
            user=request.user,
            street_address=street_address,
            city=city,
            state=state,
            pincode=pincode,
            country=country
        ).first()

        if existing_address:
            address_to_use = existing_address
            if is_default:
                Address.objects.filter(user=request.user).update(is_default=False)
                address_to_use.is_default = True
                address_to_use.save()
        else:
            address_to_use = Address.objects.create(
                user=request.user,
                street_address=street_address,
                city=city,
                state=state,
                pincode=pincode,
                country=country,
                is_default=is_default
            )
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "No product found"}, status=status.HTTP_404_NOT_FOUND)

        if quantity > product.stock_quality:
            return Response({"message": "Not Enough Stock Available"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            address=address_to_use
        )
        product.stock_quality-=quantity
        product.save()

        serializer = OrderSerializer(order)
        return Response({"message": "Order created successfully", "order": serializer.data},
                        status=status.HTTP_201_CREATED)

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"message":"order not found"}, status=status.HTTP_404_NOT_FOUND)
        order.status ='delivered'
        order.save()
        self.send_delivery_message(order.user)
        return Response({"message":"order marked and user notified"}, status=status.HTTP_200_OK)

    def send_delivery_message(self, user):
        subject = 'Order Delivered Successfully'
        message = 'Your order has been successfully delivered! Thank you for shopping with us.'
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [user.email])
        # print(f"Email sent to {user.email}:{subject}-{message}")

