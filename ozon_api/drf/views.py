from rest_framework import viewsets
from drf.models import DeliveryMethod, Cancellation, Product, Requirement, Posting
from drf.serializers import DeliveryMethodSerializer, CancellationSerializer, ProductSerializer, RequirementSerializer, PostingSerializer

class DeliveryMethodViewSet(viewsets.ModelViewSet):
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer

class CancellationViewSet(viewsets.ModelViewSet):
    queryset = Cancellation.objects.all()
    serializer_class = CancellationSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

class PostingViewSet(viewsets.ModelViewSet):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
