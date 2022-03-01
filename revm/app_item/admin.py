from django.contrib import admin
from app_item import models


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


@admin.register(models.ItemOffer)
class AdminItemOffer(admin.ModelAdmin):
    list_display = ('id', 'donor', 'name', 'subcategory')
    list_display_links = ('id', 'name')
    search_fields = ['name']

    inlines = (OtherResourceRequestInline, )

    ordering = ('pk',)

    view_on_site = False


@admin.register(models.ItemRequest)
class AdminItemRequest(admin.ModelAdmin):
    list_display = ('id', 'made_by', 'name', 'subcategory')
    list_display_links = ('id', 'name')
    search_fields = ['name']

    inlines = (OtherResourceRequestInline, )

    ordering = ('pk',)

    view_on_site = False
