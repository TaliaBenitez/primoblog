from django.urls import path
from .views import InicioListView, AboutTemplateView, ContactTemplateView, RecetaDetailView, ComentarioView,CategoriaListView, UserListView, RecetaCreateView

app_name='apps.blog'

urlpatterns = [
    path(
        route='',
        view=InicioListView.as_view(),
        name='inicio'
    ),

    path(
        route='about/',
        view=AboutTemplateView.as_view(),
        name='about'
    ),
    path(
        route='contact/',
        view=ContactTemplateView.as_view(),
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
]