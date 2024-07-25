from django.urls import path
from .views import index, pegar_detalhes

urlpatterns = [
    path('', index, name='index'),
    path('detalhes/<str:foto>/<int:id>/', pegar_detalhes, name='detalhes') 
]