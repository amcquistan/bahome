from datetime import datetime

from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, reverse

from django.views import View

from blog.models import BlogPost

from .models import Category, Tag


robots = """
User-agent: *
Allow: /
Sitemap: https://babyasst.com/sitemap.xml
"""

DOMAIN_NAME = 'https://babyasst.com'


class RobotsView(View):
    def get(self, request):
        return HttpResponse(robots, content_type="text/plain")


class SiteMapView(View):
    def get(self, request):
        posts = BlogPost.objects.filter(publish_at__lte=datetime.today()).all()

        pages = [
          f"<url><loc>{DOMAIN_NAME}{reverse('home')}</loc><lastmod>2019-06-09</lastmod><changefreq>monthly</changefreq></url>",
          f"<url><loc>{DOMAIN_NAME}{reverse('about')}</loc><lastmod>2019-06-09</lastmod><changefreq>monthly</changefreq></url>",
          f"<url><loc>{DOMAIN_NAME}{reverse('blog:posts')}</loc><lastmod>2019-06-09</lastmod><changefreq>monthly</changefreq></url>"
        ]

        for post in posts:
            pages.append(f"""
            <url>
              <loc>{DOMAIN_NAME}{reverse('blog:post', args=(post.url_slug, ))}</loc>
              <lastmod>{post.publish_at.strftime('%Y-%m-%d')}</lastmod>
              <changefreq>monthly</changefreq>
            </url>""")
        
        urls = '\n'.join(pages)
        site_map = f"""<?xml version="1.0" encoding="UTF-8"?>
          <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            {urls}
          </urlset>"""

        return HttpResponse(site_map, content_type='application/xml')


class HomeView(View):
    def get(self, request):
        return render(request, 'webapp/home.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'webapp/about.html')


class FAQsView(View):
    def get(self, request):
        return render(request, 'webapp/faqs.html')


class VideoTutsView(View):
    def get(self, request):
        return render(request, 'webapp/video_tuts.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'webapp/contact.html')

class PrivacyView(View):
    def get(self, request):
        return render(request, 'webapp/privacy.html')


class TermsView(View):
    def get(self, request):
        return render(request, 'webapp/tos.html')
