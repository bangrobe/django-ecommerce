from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from .models import Product, Variation

# Register your models here.

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductImportExportAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

class ProductAdmin(ImportExportMixin,admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('product_name',)}
    list_display = ('product_name', 'slug', 'price', 'stock', 'category')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category','variation_value', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category','variation_value', 'is_active',)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)