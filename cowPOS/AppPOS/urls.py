from django.urls import path
from . import views

app_name = 'AppPOS'
urlpatterns = [
    path('', views.pos_page, name='POS_page'),
    path('results/', views.results_page, name="results"),
    path('order/', views.order_page, name="order"),
]