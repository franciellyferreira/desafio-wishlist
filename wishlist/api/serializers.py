from rest_framework import serializers

from .models import Client, Wishlist


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name', 'email',)


class WishlistSerializerOutput(serializers.ModelSerializer):
    id = serializers.CharField(max_length=36)
    title = serializers.CharField(max_length=100, default='')
    price = serializers.FloatField(default=0.0)
    image = serializers.CharField(max_length=254, default='')
    brand = serializers.CharField(max_length=100, default='')

    class Meta:
        model = Wishlist
        fields = ('id', 'title', 'price', 'image', 'brand')


class WishlistSerializerInput(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
