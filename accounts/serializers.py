from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Product, Order, Address


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    gender = serializers.CharField()
    phone_no = serializers.CharField(max_length=10, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'confirm_password', 'gender', 'phone_no', 'first_name', 'last_name',
                  'is_seller']

    def validate_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("phone number must be 10 digits")
        if not value.isdigit():
            raise serializers.ValidationError("phone number contain 10 digits")
        return value


    def validate(self, attrs):
        password = attrs.get('password')
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
                                           # jo user model hai vo blank ko v accept krta hai isliy hmne fer jha pr validation lga de hai
        if first_name is None or first_name == '':
            raise serializers.ValidationError({"first_name": "first_name is required"})
        if last_name is None or last_name == '':
            raise serializers.ValidationError({"last_name": "last_name is required"})
        return attrs

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        user = get_user_model().objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"email": "the email not exist"})
        if not user.is_active:
            raise serializers.ValidationError({"email": "user not verified"})
        if not user.check_password(password):
            raise serializers.ValidationError({"email": "invalid detail"})
        attrs['user'] = user
        return attrs


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'phone_no', 'gender', 'is_seller']


class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    user_id = serializers.IntegerField(required=True)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'pincode', 'country']


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







# class ProductSerializer(serializers.ModelSerializer):
#     owner = userSerializer(read_only=True)
#     class Meta:
#         model = Product
#         # fields = '__all__'
#         fields = ['id', 'name', 'description', 'price', 'stock_quality', 'owner']
#         read_only_fields = ('owner',)
#     def validate(self, attrs):
#         price = attrs.get('price')
#         if price is None:
#             raise serializers.ValidationError({"price": "price not null"})
#         return attrs
# class OrderSerializer(serializers.ModelSerializer):
#     user = userSerializer(read_only=True)
#     product = ProductSerializer(read_only=True)
#     class Meta:
#         model = Order
#         fields = '__all__'
#         read_only_fields = ('user', 'created_at')
#     def validate(self, attrs):
#         quantity = attrs.get('quantity')
#         if quantity <=0:
#             raise serializers.ValidationError({"Quantity": "Quantity Must Be Grater Then Zero"})
#         return attrs