from django.contrib.auth.models import AbstractUser


from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)


class NewPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="new_posts")
    post_text = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date} by {self.user}"