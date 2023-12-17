from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from django.contrib.auth.models import User
from apps.users.models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'imagen')
    list_display_links = ('pk', 'user',)
    list_editable = ('imagen',)

    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'users__last_name',
    )

    list_filter = (
        'user__is_active',
        'user__is_staff',
        'modificado',
    )

    fieldsets = (
        ('Perfil', {
            'fields': (('user', 'imagen'),),
        }),
        ('Extra info', {
            'fields': (('modificado'),),
        })
    )

    readonly_fields = ('modificado',)

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfiles'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
