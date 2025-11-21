# Добавить модель "Производитель" (Manufacturer) с полями: название, страна, описание. Связать с моделью Product.

from django.contrib import admin
from .models import Category, Product, Manufacturer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name", "description")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "manufacturer", "price",
        "is_available", "created_at"
    )
    list_filter = ("category", "manufacturer", "is_available", "created_at")
    search_fields = ("name", "description")
    list_editable = ("price", "is_available")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "description", "category", "manufacturer")
        }),
        ("Цена и доступность", {
            "fields": ("price", "is_available")
        }),
        ("Изображение", {
            "fields": ("image",)
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )

@admin.register(Manufacturer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "description")
    list_filter = ("name", "country")
    search_fields = ("name", "country", "description")