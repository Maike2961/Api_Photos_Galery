from django.urls import path
from .views import index, pegar_detalhes, limpar

urlpatterns = [
    path('', index, name='index'),
    path('limpar/', limpar, name='limpar'),
    path('detalhes/<str:foto>/<int:id>/', pegar_detalhes, name='detalhes') 
]