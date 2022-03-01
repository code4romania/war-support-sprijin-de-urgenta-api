from django.contrib import admin
from app_other import models


class OtherResourceRequestInline(admin.TabularInline):
    model = models.ResourceRequest
    extra = 0
    show_change_link = True
    view_on_site = True


@admin.register(models.Category)
class AdminOtherRequest(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ['name']

    ordering = ('pk',)

    view_on_site = False


@admin.register(models.Subcategory)
class AdminOtherRequest(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('id', 'name')
    search_fields = ['name']

    ordering = ('pk',)

    view_on_site = False


@admin.register(models.OtherOffer)
class AdminOtherOffer(admin.ModelAdmin):
    list_display = ('id', 'name', 'subcategory')
    list_display_links = ('id', 'name')
    search_fields = ['name']

    inlines = (OtherResourceRequestInline, )

    ordering = ('pk',)

    view_on_site = False


@admin.register(models.OtherRequest)
class AdminOtherRequest(admin.ModelAdmin):
    list_display = ('id', 'name', 'subcategory')
    list_display_links = ('id', 'name')
    search_fields = ['name']

    inlines = (OtherResourceRequestInline, )

    ordering = ('pk',)

    view_on_site = False
