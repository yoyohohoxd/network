from django.contrib import admin

from .models import User, NewPost, Profile

admin.site.register(User)
admin.site.register(NewPost)
admin.site.register(Profile)