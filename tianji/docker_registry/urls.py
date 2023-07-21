from django.urls import path
from .views import IndexView, RegistryView

urlpatterns = [
    path('images-list', IndexView.as_view(), name='docker_registry_images_list'),
    path('notify-url', RegistryView.as_view())
]