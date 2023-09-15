from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cluster-images', ClusteringImagesViewSets)
router.register(r'logistic-images', LogisticImagesViewSets)

app_name = 'app'

urlpatterns = [
    path('', include(router.urls), name='images'),
    path('clustering/', CustomerClusteringView.as_view(), name='clustering'),
    path('api/clustering/', CustomerClusteringApiView.as_view(), name='clustering_api'),
    path('api/churn/', CustomerChurnViewApiView.as_view(), name='churn_api'),
    path('api/churn/train', TrainChurnApiView.as_view(), name='churn_train'),
    path('api/churn/test', TestChurnApiView.as_view(), name='churn_test')
]
