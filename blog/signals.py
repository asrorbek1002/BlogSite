# blog/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import PostView, Post

@receiver(post_save, sender=Post)
def create_post_view(sender, instance, created, **kwargs):
    if created:
        PostView.objects.create(post=instance)