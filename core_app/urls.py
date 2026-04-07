from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('api/ads/', views.api_ads_feed, name='api_ads_feed'),
    path('ads/all/', views.all_ads_page, name='all_ads_page'),
    path('ads/category/<int:pk>/', views.ads_by_category, name='ads_by_category'),
    path('ads/search/', views.search_page, name='search_page'),
    path('ads/search/results/', views.search_results, name='search_results'),
    path('ads/read/<uuid:uuid>/', views.read_ad_page, name='read_ad_page'),
    path('ads/new/', views.ad_create_view, name='ad_create'),
    path('ads/<uuid:uuid>/edit/', views.ad_update_view, name='ad_update'),
    path('ads/<uuid:uuid>/delete/', views.ad_delete_view, name='ad_delete'),
    path('ads/<uuid:uuid>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('ads/<uuid:uuid>/review/', views.submit_review, name='submit_review'),
    path('profile/', views.profile_page, name='profile_page'),
    path('register/', views.register_view, name='register_page'),
    path('login/', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout_view'),
]
