# blog/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts', through='PostCategory')
    tags = models.ManyToManyField('Tag', related_name='posts', through='PostTag')

class PostContent(models.Model):
    POSTCONTENT_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='contents')
    type = models.CharField(max_length=10, choices=POSTCONTENT_TYPES)
    order = models.PositiveIntegerField()  # tartib raqami, qaysi blok birinchi chiqishini belgilaydi
    text = models.TextField(blank=True, null=True)  # agar type='text' bo‘lsa
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # type='image' bo‘lsa

    class Meta:
        ordering = ['order']  # tartib bilan chiqishi uchun
    def __str__(self):
        return f"{self.post.title} - {self.get_type_display()} - {self.order}"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'tag')


class PostView(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='view_data')
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('spam', 'Spam')
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    comment_body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_body[:30]
