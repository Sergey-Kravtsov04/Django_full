from django.contrib import admin
from .models import BlogPost,Comment
from django.contrib.auth.models import Permission

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Permission)
