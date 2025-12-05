from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Report


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'author', 'created_at')
    list_filter = ('category', 'author')
    search_fields = ('category', 'message', 'author__username')
