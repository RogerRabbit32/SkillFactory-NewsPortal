from django.contrib import admin
from .models import Category, Post, Comment, Author, PostCategory, Subscribers


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_text', 'creation_date', 'post_rating')
    list_filter = ('author', 'post_type')
    search_fields = ('title',)


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Subscribers)
