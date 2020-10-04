from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Article
from datetime import datetime


# admin.site.register(Article)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "date_create",
                    "date_change", "date_pub", "status")
    readonly_fields = ("get_img", "author", "date_pub", "status")

    def get_img(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="200", heght="200">')
    get_img.short_description = "Картинка"

    actions = ["publish", "unpublish"]

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(
            status=Article.STATUS.DRAFT, date_pub=None)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(
            status=Article.STATUS.PUBLISHED, date_pub=datetime.now())
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)
