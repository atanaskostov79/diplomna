from django.contrib import admin

from posts.models import Category, Comment, Posts


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('entry_title', 'category', 'created_at')
    list_filter = ('category',)
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
