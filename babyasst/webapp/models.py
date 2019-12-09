from django.conf import settings
from django.db import models
from django.utils.timezone import now

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Publishable(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    url_slug = models.CharField(max_length=50, unique=True)
    publish_at = models.DateTimeField(default=now)
    expire_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Likable(models.Model):
    likes = models.IntegerField(default=1)

    class Meta:
        abstract = True


class Category(TimeStamped, Publishable):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Tag(TimeStamped, Publishable):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title