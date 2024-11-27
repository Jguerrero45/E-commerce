from rest_framework import serializers
from .models import Product, Dimension, MetaInfo, Review, Tags

class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = ('width', 'height', 'depth')

class MetaInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaInfo
        fields = ('barcode', 'qr_code')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'comment', 'reviewer_name', 'reviewer_email')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')

class ProductSerializer(serializers.ModelSerializer):
    dimensions = DimensionSerializer(required=False)
    meta_info = MetaInfoSerializer(required=False)
    reviews = ReviewSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description', 'category', 'price', 'discount_percentage', 
            'rating', 'stock', 'tags', 'brand', 'sku', 'weight', 'warranty_information', 
            'shipping_information', 'availability_status', 'return_policy', 
            'minimum_order_quantity', 'images', 'thumbnail', 'dimensions', 
            'meta_info', 'reviews'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        dimension_data = validated_data.pop('dimensions', None)
        meta_info_data = validated_data.pop('meta_info', None)

        product = Product.objects.create(**validated_data)

        for tag_data in tags_data:
            if 'id' in tag_data:  
                tag = Tags.objects.get(id=tag_data['id'])
            else:  
                tag, created = Tags.objects.get_or_create(**tag_data)
            product.tags.add(tag)

        if dimension_data:
            Dimension.objects.create(product=product, **dimension_data)
        if meta_info_data:
            MetaInfo.objects.create(product=product, **meta_info_data)

        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return representation
