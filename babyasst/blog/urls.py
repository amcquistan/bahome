
from django.urls import path

from . import views

# this is required for namespaced URLConf include
app_name='blog'

urlpatterns = [
  path('', views.PostsListView.as_view(), name='posts'),
  path('category/<str:url_slug>/', views.PostsByCategoryView.as_view(), name='posts_by_category'),
  path('tag/<str:url_slug>/', views.PostsByTagView.as_view(), name='posts_by_tag'),
  path('<str:url_slug>/', views.PostDetailsView.as_view(), name='post'),
  path('preview/<str:url_slug>/', views.PostPreviewDetailsView.as_view(), name='post_preview'),
  path('<str:url_slug>/like/', views.LikePostView.as_view(), name='like_post')
]