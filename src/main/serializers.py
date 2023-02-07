from rest_framework import serializers

from main.models import Product, ProductType


class SearchProductsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ('name', 'image', 'url')
        depth = 1

    def get_name(self, obj):
        return obj.name.title()

    def get_url(self, obj):
        return obj.get_absolute_url
    
    def get_image(self, obj):
        return obj.image.url


class SearchTypesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductType
        fields = ('name', 'url')

    def get_name(self, obj):
        return obj.name.capitalize()

    def get_url(self, obj):
        return obj.get_absolute_url


class SearchCategoriesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductType
        fields = ('name', 'url')
    
    def get_name(self, obj):
        return obj.name.capitalize()
    
    def get_url(self, obj):
        return obj.get_absolute_url
    