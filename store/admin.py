from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Category, Cart, Wishlist, Order, OrderItem, Profile

# ✅ Restrict admin access to superusers only
class CustomUserAdmin(UserAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser  # ✅ Only superusers can add users

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # ✅ Only superusers can modify users

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # ✅ Restrict deletions to superusers

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
