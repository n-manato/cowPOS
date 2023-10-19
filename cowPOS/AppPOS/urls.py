from django.urls import path
from . import views

app_name = 'app_folder'
urlpatterns = [
    path('pos_page/', views.pos_page, name='POS_page'),
    path('results/', views.results_page, name="results"),
]