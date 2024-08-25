from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search', views.search, name='search'),
    path('most-popular-companies', views.most_popular_companies, name='popular-companies')
]
