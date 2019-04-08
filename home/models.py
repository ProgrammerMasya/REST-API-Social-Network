from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(verbose_name="Нравится", default=0)
    dislikes = models.IntegerField(verbose_name="Не нравится", default=0)

    def __str__(self):
        return str(self.post)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
