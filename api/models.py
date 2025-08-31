from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    POST_TYPE = [
        ('blog', 'Blog'),
        ('project', 'Project'),
        ('ai-generated', 'AI Generated'),
    ]

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    post_type = models.CharField(max_length=20, choices=POST_TYPE)

    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        default='post_images/default.png'
    )
    tags = models.CharField(max_length=200, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class PostSection(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='sections')
    order = models.PositiveIntegerField()  
    title = models.CharField(max_length=150)
    description = models.TextField()

    class Meta:
        ordering = ['order']  

    def __str__(self):
        return f"{self.post.title} - Section {self.order}: {self.title}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user') 

    def __str__(self):
        return f"{self.user} liked {self.post}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented on {self.post}"
