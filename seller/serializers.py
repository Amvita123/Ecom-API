from rest_framework import serializers
from accounts.models import Product, Order
from accounts.serializers import userSerializer, AddressSerializer


class ProductSerializer(serializers.ModelSerializer):
    # owner = userSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quality']
        read_only_fields = ('owner',)

    def validate(self, attrs):
        price = attrs.get('price')
        if price is None:
            raise serializers.ValidationError({"price": "price not null"})
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    # user = userSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    address = AddressSerializer()
    seller = userSerializer(source='product.owner', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'product', 'quantity', 'address', 'seller']
        read_only_fields = ('created_at',)

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        if quantity <=0:
            raise serializers.ValidationError({"Quantity": "Quantity Must Be Grater Then Zero"})
        return attrs





