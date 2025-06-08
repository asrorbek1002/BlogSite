from django.contrib import admin
from .models import Post, PostContent, Category, Tag, PostCategory, PostTag, Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'comment_body')
    raw_id_fields = ('post',)
    ordering = ('-created_at',)

class PostContentInline(admin.TabularInline):
    model = PostContent
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostContentInline]
    list_display = ('title', 'status', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostCategory)
admin.site.register(PostTag)
