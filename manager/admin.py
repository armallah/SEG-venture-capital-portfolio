from django.contrib import admin
from .models import User

from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class MyModelAdmin(UserAdmin):
    
    admin.site.site_title = "Venture Capital Porfolio"

    perm_fields = ('is_active', 'user_type', 'is_superuser',
                        'groups', 'user_permissions')
    
    fieldsets = (
        (None, {
            'fields' : ('username', 'password',),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name',),
        }),
        ('Permissions', {
            'fields': perm_fields},
         ),
        (('Important dates'), {
            'fields': ('last_login', 'date_joined',),
            'classes':('collapse',),
        }))
    
                   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2', 'user_type')}
         ),
    )
    
    list_display = ('username', 'first_name', 'last_name', 'is_superuser')
    list_filter = ('is_superuser','user_type')
    search_fields = ('username', 'first_name', 'last_name',)
    ordering = ('username',)
    filter_horizontal = ()    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)
    
    def has_add_permission(self, request):
        if (request.user.is_superuser == False):
            return False
        return True
        
    