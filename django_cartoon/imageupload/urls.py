from django.urls import path, re_path
from . import views

urlpatterns = [

    path('cartoonize/', views.img_list)

]
