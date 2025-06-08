# blog/serializers.py

from rest_framework import serializers
from .models import Post, Comment, Category, Tag, PostCategory, PostTag
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'name', 'email', 'comment_body', 'status', 'created_at', 'parent_comment', 'replies']
        read_only_fields = ['status', 'created_at', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
    
from rest_framework import serializers
from .models import Post, PostContent, Category, Tag

class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['id', 'type', 'order', 'text', 'image']

class PostSerializer(serializers.ModelSerializer):
    contents = PostContentSerializer(many=True)  # nested serializer

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'status', 'categories', 'tags', 'contents']

    def create(self, validated_data):
        contents_data = validated_data.pop('contents')
        post = Post.objects.create(**validated_data)
        for content_data in contents_data:
            PostContent.objects.create(post=post, **content_data)
        return post

    def update(self, instance, validated_data):
        contents_data = validated_data.pop('contents')
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # PostContent ni yangilash (oddiy yondashuv)
        instance.contents.all().delete()  # eski bloklarni o'chirish
        for content_data in contents_data:
            PostContent.objects.create(post=instance, **content_data)

        return instance
