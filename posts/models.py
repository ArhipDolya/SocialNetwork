from django.db import models, transaction
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    @transaction.atomic
    def like_post(self, user):
        if not self.is_liked_by(user):
            Like.objects.create(user=user, post=self)
            self.likes += 1
            self.save()
            self.refresh_from_db()

    @transaction.atomic
    def unlike_post(self, user):
        like = Like.objects.filter(user=user, post=self).first()
        if like:
            like.delete()
            self.likes -= 1
            self.save()
            self.refresh_from_db()

    def is_liked_by(self, user):
        return self.likes > 0

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    def __repr__(self):
        return f"{self.user.username} - {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post}"

    def __repr__(self):
        return f"{self.user.username} liked {self.post}"

