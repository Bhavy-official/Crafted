# api/admin.py
from django.contrib import admin
from api.models import Post, PostSection, Comment, Like

class PostSectionInline(admin.TabularInline):
    model = PostSection
    extra = 1  # Number of empty section forms initially shown
    fields = ('order', 'title', 'description')
    ordering = ('order',)
    show_change_link = True

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_type', 'created_at')
    list_filter = ('post_type', 'created_at', 'author')
    search_fields = ('title', 'description', 'tags', 'author__username')
    inlines = [PostSectionInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__username')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(PostSection)
