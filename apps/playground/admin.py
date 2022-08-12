
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
# ============================================================================ #
from apps.store.admin import ProductAdmin
from apps.tags.models import TaggedItem
from apps.store.models import Product


# ================================= TAGINLINE ================================ #

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


# ============================ CUSTOMPRODUCTADMIN ============================ #

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


# ================================= REGISTER ================================= #

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)

