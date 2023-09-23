from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Accountant


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_accountant', 'is_teacher',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_accountant', 'is_teacher',)
    fieldsets = (
        (None, {'fields': ('first_name', 'middle_name', 'last_name','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_accountant', 'is_teacher',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_accountant', 'is_teacher',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Accountant)