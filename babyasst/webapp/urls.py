from django.urls import path
from . import views

urlpatterns = [
  path('', views.HomeView.as_view(), name='home'),
  path('robots.txt', views.RobotsView.as_view(), name='robots'),
  path('sitemap.xml', views.SiteMapView.as_view(), name='sitemap'),
  path('about/', views.AboutView.as_view(), name='about'),
  path('privacy/', views.PrivacyView.as_view(), name='privacy'),
  path('terms/', views.TermsView.as_view(), name='tos'),
]