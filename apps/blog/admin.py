from django.contrib import admin
from .models import Receta, Categoria, Comentario


# Registrando los modelos.

@admin.register(Receta)

class RecetaAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'plato', 'categoria',
                    'destacada', 'publish', 'imagen','status')
    search_fields = ('plato', 'user__username', 'user__email')
    list_filter = ('creado', 'modificado')
    list_editable = ('plato','categoria', 'destacada', 'publish','status')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('url',)
        form = super(RecetaAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['perfil'].initial = request.user.perfil
        return form

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'receta', 'comentario', 'visible')