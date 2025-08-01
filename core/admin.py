from django.contrib import admin
from django.utils.html import format_html
from .models import Library, User, Category, Product, Cart, CartItem, Order

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'slug', 'desks_count')
    fields = ('name', 'slug', 'address', 'description', 'desks_count', 'admins') 
    filter_horizontal = ('admins',) 

    def get_readonly_fields(self, request, obj=None):
        if obj: 
            return ('slug',)
        return ()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'full_name', 'phone_number', 'created_at')
    search_fields = ('telegram_id', 'full_name', 'phone_number')
    list_filter = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'products_count')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Mahsulotlar soni'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'image_preview')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Rasm'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'is_active', 'total_price')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__telegram_id', 'user__full_name')

    def total_price(self, obj):
        return f"{obj.total_price} so'm"
    total_price.short_description = 'Jami narx'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'total_price')
    list_filter = ('cart__user',)
    
    def total_price(self, obj):
        return f"{obj.total_price} so'm"
    total_price.short_description = 'Jami narx'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'library', 'desk_number', 'status', 'created_at', 'total_price')
    list_filter = ('status', 'created_at', 'library')
    search_fields = ('user__telegram_id', 'user__full_name', 'desk_number')
    readonly_fields = ('created_at', 'updated_at')
    
    def total_price(self, obj):
        return f"{obj.total_price} so'm"
    total_price.short_description = 'Jami narx'