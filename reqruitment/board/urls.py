from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardView

router = DefaultRouter()
router.register(r'board', BoardView)

urlpatterns = [
    path('', include(router.urls))
]