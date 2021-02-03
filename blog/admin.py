from django.contrib import admin
from .models import Post, Suggestion

admin.site.register(Post)
admin.site.register(Suggestion)
admin.site.site_header = "MemeBank Admin"
admin.site.site_title = "MemeBank Admin Portal"