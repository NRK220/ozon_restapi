from rest_framework import serializers
from drf.models import DeliveryMethod, Cancellation, Product, Requirement, Posting

class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = '__all__'

class CancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancellation
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'

class PostingSerializer(serializers.ModelSerializer):
    delivery_method = DeliveryMethodSerializer()
    cancellation = CancellationSerializer()
    products = ProductSerializer(many=True)
    requirements = RequirementSerializer()

    class Meta:
        model = Posting
        fields = '__all__'

    def create(self, validated_data):
        delivery_method_data = validated_data.pop('delivery_method')
        cancellation_data = validated_data.pop('cancellation')
        products_data = validated_data.pop('products')
        requirements_data = validated_data.pop('requirements')

        delivery_method, _ = DeliveryMethod.objects.get_or_create(**delivery_method_data)
        cancellation, _ = Cancellation.objects.get_or_create(**cancellation_data)
        requirements, _ = Requirement.objects.get_or_create(**requirements_data)

        posting = Posting.objects.create(
            delivery_method=delivery_method,
            cancellation=cancellation,
            requirements=requirements,
            **validated_data
        )

        product_instances = []
        for product_data in products_data:
            product, _ = Product.objects.get_or_create(**product_data)
            product_instances.append(product)
        
        posting.products.set(product_instances)
        return posting

    def update(self, instance, validated_data):
        delivery_method_data = validated_data.pop('delivery_method')
        cancellation_data = validated_data.pop('cancellation')
        products_data = validated_data.pop('products')
        requirements_data = validated_data.pop('requirements')

        DeliveryMethod.objects.filter(id=instance.delivery_method.id).update(**delivery_method_data)
        Cancellation.objects.filter(cancel_reason_id=instance.cancellation.cancel_reason_id).update(**cancellation_data)
        Requirement.objects.filter(id=instance.requirements.id).update(**requirements_data)

        instance.delivery_method.refresh_from_db()
        instance.cancellation.refresh_from_db()
        instance.requirements.refresh_from_db()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        product_instances = []
        for product_data in products_data:
            product, _ = Product.objects.get_or_create(**product_data)
            product_instances.append(product)

        instance.products.set(product_instances)
        return instance
