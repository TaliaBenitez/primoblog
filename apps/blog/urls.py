from django.urls import path
from .views import InicioListView, NosotrosTemplateView, ContactoTemplateView, RecetaDeleteView, RecetaDetailView, ComentarioView,CategoriaListView, UserListView, RecetaCreateView, RecetaUpdateView

app_name='apps.blog'

urlpatterns = [
    path(
        route='',
        view=InicioListView.as_view(),
        name='inicio'
    ),

    path(
        route='nosotros/',
        view=NosotrosTemplateView.as_view(),
        name='nosotros'
    ),
    path(
        route='contacto/',
        view=ContactoTemplateView.as_view(),
        name='contacto'
    ),
    path(
        route='receta/<slug:url>/',
        view=RecetaDetailView.as_view(),
        name='detalle'
    ),
    path(
        route='carga_receta/',
        view=RecetaCreateView.as_view(),
        name='carga_receta'
    ),
    path(
        route='comentario/',
        view=ComentarioView.as_view(),
        name='comentario'
    ),
    path(
        route='categoria/<int:categoria_id>/',
        view=CategoriaListView.as_view(),
        name='categoria'
    ),
    path(
        route='user/<str:nombre>/',
        view=UserListView.as_view(),
        name='user'
    ),
    path(
        route='eliminar_receta/<slug:url>/',
        view=RecetaDeleteView.as_view(),
        name='eliminar_receta'
    ),
    path(
        route='actualizar_receta/<slug:url>/',
        view=RecetaUpdateView.as_view(),
        name='actualizar_receta'
    ),
]