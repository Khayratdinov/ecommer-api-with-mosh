from apps.store.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from apps.store.admin import ProductAdmin
from apps.tags.models import TaggedItem


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
