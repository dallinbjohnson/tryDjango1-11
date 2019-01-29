"""muypicky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from .views import (
  RestaurantListView,
  RestaurantDetailView,
  # restaurant_createview,
  RestaurantCreateView,
  RestaurantUpdateView,
)

app_name = "restaurants"
urlpatterns = [
    url(r'^$', RestaurantListView.as_view(), name='index'),
    # url(r'^restaurants/create/$', restaurant_createview),
    url(r'^create/$', RestaurantCreateView.as_view(), name='create'),
    # url(r'^(?P<slug>\w+)/$', RestaurantListView.as_view()),
    # url(r'^(?P<pk>\w+)/$', RestaurantDetailView.as_view()),
    # url(r'^(?P<rest_id>\w+)/$', RestaurantDetailView.as_view()),
    url(r'^(?P<slug>[\w-]+)/$', RestaurantDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', RestaurantUpdateView.as_view(), name='update'),
]
