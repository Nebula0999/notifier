from django.urls import path
from . import views
 
urlpatterns = [
  path('', views.data_wall, name='data-wall'),
  path('proxy-image/', views.proxy_image, name='proxy-image'),
]