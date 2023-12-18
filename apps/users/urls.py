from django.urls import path

from .views import LoginView, RegistroView, RegistroOkTemplateView, SalirView

app_name='apps.users'

urlpatterns = [
    path(
        route='login',
        view=LoginView.as_view(),
        name='login'
    ),
    path(
        route='registro',
        view=RegistroView.as_view(),
        name='registro'
    ),
    path(
        route='salir/',
        view=SalirView.as_view(),
        name='salir'
    ),
    path(
        route='registro_completado/',
        view=RegistroOkTemplateView.as_view(),
        name='registrook'
    ),
    
]