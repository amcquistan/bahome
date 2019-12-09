from django.urls import path
from . import views

urlpatterns = [
  path('', views.HomeView.as_view(), name='home'),
  path('robots.txt', views.RobotsView.as_view(), name='robots'),
  path('sitemap.xml', views.SiteMapView.as_view(), name='sitemap'),
  path('about/', views.AboutView.as_view(), name='about'),
  path('contact/', views.ContactView.as_view(), name='contact'),
  path('faqs/', views.FAQsView.as_view(), name='faqs'),
  path('video-tutorials/', views.VideoTutsView.as_view(), name='video_tuts'),
  path('privacy/', views.PrivacyView.as_view(), name='privacy'),
  path('terms/', views.TermsView.as_view(), name='tos'),
]