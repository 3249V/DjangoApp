from django.contrib import admin
from .models import Post

admin.site.register(Post)
admin.site.site_header = "MemeBank Admin"
admin.site.site_title = "MemeBank Admin Portal"