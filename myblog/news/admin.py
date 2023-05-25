from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['title', 'body']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}  # нужно пред-заполнять поле slug данными, вводимыми в поле title
    raw_id_fields = ['author']
    date_hierarchy = 'publish'  # навигационные ссылки для навигации по иерархии дат;
    ordering = ['status', 'publish']
