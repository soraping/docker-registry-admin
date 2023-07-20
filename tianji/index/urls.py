from django.urls import path
from tianji.index import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('index', views.IndexView.as_view()),
]