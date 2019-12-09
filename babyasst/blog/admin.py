from django.contrib import admin

from .models import BlogPost

class TinyMCEAdmin(admin.ModelAdmin):
    class Media:
        js = ('/static/js/tinymce/tinymce.min.js', '/static/js/tinymce/admin_textareas.js', '/static/js/prism/prism.js')
        css = {'all': ('/static/css/prism/prism.css',)}

admin.site.register(BlogPost, TinyMCEAdmin)
