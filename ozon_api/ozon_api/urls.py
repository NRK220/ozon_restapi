from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf import views

router = DefaultRouter()
router.register(r'deliverymethods', views.DeliveryMethodViewSet)
router.register(r'cancellations', views.CancellationViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'requirements', views.RequirementViewSet)
router.register(r'postings', views.PostingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
