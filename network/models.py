from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class NewPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="new_posts")
    post_text = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.date} by {self.user}"