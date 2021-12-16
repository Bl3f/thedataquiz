from django.contrib import admin

from app.models import Tag, Question


class TagAdmin(admin.ModelAdmin):
    list_display = ('slug', 'display')


admin.site.register(Tag, TagAdmin)
admin.site.register(Question)

