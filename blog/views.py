# blog/views.py

from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Category, Tag, PostView
from .serializers import PostSerializer, CommentSerializer, CategorySerializer, TagSerializer
from .permissions import IsAdminOrReadOnly
from .utils import notify_admin_telegram

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related('categories', 'tags').all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['categories', 'tags']  # filtering uchun
    search_fields = ['title', 'contents__text']  # qidiruv uchun

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        post_view, created = PostView.objects.get_or_create(post=post)
        post_view.like_count += 1
        post_view.save()
        return Response({'like_count': post_view.like_count})

    @action(detail=True, methods=['get'])
    def increment_view(self, request, pk=None):
        post = self.get_object()
        post_view, created = PostView.objects.get_or_create(post=post)
        post_view.view_count += 1
        post_view.save()
        return Response({'view_count': post_view.view_count})

    @action(detail=False, methods=['get'])
    def top(self, request):
        top_posts = Post.objects.filter(status='published') \
                        .annotate(like_count=Count('view_data__like_count')) \
                        .order_by('-view_data__like_count')
        page = self.paginate_queryset(top_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(top_posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        parent_comment = serializer.validated_data.get('parent_comment')
        comment = serializer.save(user=self.request.user if self.request.user.is_authenticated else None)
        notify_admin_telegram(comment)
        if parent_comment:
            parent_comment.send_reply_notification()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
