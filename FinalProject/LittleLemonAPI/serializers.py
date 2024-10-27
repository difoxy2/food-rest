from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.MenuItem
        fields = ['id','title','price','featured','category','category_id']
        extra_kwargs = {'price': {'min_value': 0.1}}

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.Cart
        fields = ['menuitem','menuitem_id','quantity','user','unit_price','price']
        extra_kwargs = {'quantity': {'min_value': 0}}

class OrderSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    user_id=serializers.IntegerField(write_only=True)
    delivery_crew=serializers.StringRelatedField()
    class Meta:
        model=models.Order
        fields=['id','user','user_id','delivery_crew','status','total','date']

class OrderPUTSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    delivery_crew=serializers.StringRelatedField(read_only=True)
    user_id=serializers.IntegerField(write_only=True)
    delivery_crew_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=models.Order
        fields=['id','user','user_id','delivery_crew','delivery_crew_id','status','total','date']
        extra_kwargs = {
            'user': {'required': True},
            'delivery_crew': {'required': True},
            'status': {'required': True},
            'total': {'required': True},
            }

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model=models.OrderItems
        fields = ['menuitem','menuitem_id','quantity','order','unit_price','price']