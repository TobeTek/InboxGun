from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    date_hierachy = "publish"
    ordering = ("status", "publish")
