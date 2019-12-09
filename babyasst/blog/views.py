from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from webapp.models import Category, Tag
from .models import BlogPost

POSTS_PER_PAGE = 5

class PostsListView(View):
    def get(self, request):
        all_posts = BlogPost.objects.filter(publish_at__lte=datetime.today()).all()

        paginator = Paginator(all_posts, POSTS_PER_PAGE)
        page = request.GET.get('page', 1)
        posts = paginator.get_page(page)

        context = get_posts_common_context(posts)
        return render(request, 'blog/posts.html', context)


class PostDetailsView(View):
    def get(self, request, url_slug):
        post = BlogPost.objects.get(url_slug=url_slug)

        category = post.categories.first()
        context = get_posts_common_context([post])

        context['post'] = post
        context['favorite_category_posts'] = get_favorite_posts(category.blog_posts.all(), limit=3)
        context['prev_post'] = get_previous_post(post)
        context['next_post'] = get_next_post(post)
        context['twitter_link'] = twitter_share_link(request, post)
        context['facebook_link'] = facebook_share_link(request)
        context['linkedin_link'] = linkedin_share_link(request, post)

        
        return render(request, 'blog/post.html', context)


class PostPreviewDetailsView(View):
    def get(self, request, url_slug):
        post = BlogPost.objects.get(url_slug=url_slug)
        return render(request, 'blog/post.html', { 'post': post })


class PostsByCategoryView(View):
    def get(self, request, url_slug):
        category = Category.objects.get(url_slug=url_slug)
        all_posts = []
        if category:
            all_posts = category.blog_posts.filter(publish_at__lte=datetime.today()).order_by('id').all()

        paginator = Paginator(all_posts, POSTS_PER_PAGE)
        page = request.GET.get('page', 1)
        posts = paginator.get_page(page)

        context = get_posts_common_context(posts)
        context['category'] = category
        return render(request, 'blog/posts.html', context)


class PostsByTagView(View):
    def get(self, request, url_slug):
        tag = Tag.objects.get(url_slug=url_slug)
        all_posts = []
        if tag:
            all_posts = tag.blog_posts.filter(publish_at__lte=datetime.today()).order_by('id').all()

        paginator = Paginator(all_posts, POSTS_PER_PAGE)
        page = request.GET.get('page', 1)
        posts = paginator.get_page(page)

        context = get_posts_common_context(posts)
        context['tag'] = tag
        return render(request, 'blog/posts.html', context)


class LikePostView(View):
    def get(self, request, url_slug):
        post = BlogPost.objects.get(url_slug=url_slug)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})


def get_posts_common_context(posts):
    categories = {}
    tags = {}
    
    posts_for_metadata = BlogPost.objects.all()
    for post in posts_for_metadata:
        for category in post.categories.all():
            if category.id not in categories:
                category.post_count = 0
                categories[category.id] = category

            categories[category.id].post_count += 1

        for tag in post.tags.all():
            if tag.id not in tags:
                tag.post_count = 0
                tags[tag.id] = tag

            tags[tag.id].post_count += 1

    limit = 5

    return {
      'posts': posts,
      'categories': categories,
      'tags': list(tags.values()),
      'recent_posts': posts_for_metadata[:limit],
      'favorite_posts': get_favorite_posts(posts_for_metadata, limit)
    }


def get_favorite_posts(posts, limit=5):
    return sorted(posts, key=lambda post: post.likes, reverse=True)[:limit]


def get_previous_post(post):
    return BlogPost.objects.filter(
        publish_at__lt=post.publish_at
      ).order_by('-publish_at').first()


def get_next_post(post):
    return BlogPost.objects.filter(
        publish_at__gt=post.publish_at,
        publish_at__lte=datetime.today()
      ).order_by('publish_at').first()


def twitter_share_link(request, post):
    title = '%20'.join(post.title.split())
    url = request.build_absolute_uri()
    link = f"https://twitter.com/share?text={title}&url={url}"
    return link


def linkedin_share_link(request, post):
    title = '%20'.join(post.title.split())
    source = "https://thecodinginterface.com"
    url = request.build_absolute_uri()
    link = f"https://www.linkedin.com/shareArticle?mini=true&url={url}&title={title}&source={source}"
    return link


def facebook_share_link(request):
    link = f"https://www.facebook.com/sharer/sharer.php?u={request.build_absolute_uri()}"
    return link