from django.db import models
from django.conf import settings

from webapp.models import TimeStamped, Publishable, Category, Tag, Likable

class BlogPost(TimeStamped, Publishable, Likable):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name='blog_posts')
    tags = models.ManyToManyField(Tag, related_name='blog_posts')
    feature_img_url = models.CharField(max_length=500, null=True, blank=True)

    def author_display_name(self):
        if self.created_by.first_name:
            return self.created_by.first_name + " " + self.created_by.last_name
        return self.created_by.username

    def __str__(self):
        return self.title
