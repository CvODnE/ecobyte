from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FoodListing, FoodClaim, Review, DonorProfile, CollectorProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'user_type', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(FoodListing)
admin.site.register(FoodClaim)
admin.site.register(Review)
admin.site.register(DonorProfile)
admin.site.register(CollectorProfile)
