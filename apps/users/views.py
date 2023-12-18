from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import RegistroForm

class RegistroView(FormView):
    form_class = RegistroForm
    template_name = 'user/registro.html'
    success_url = reverse_lazy('auth:registrook')

    def form_valid(self, form):
        try:
            # Intenta crear y guardar el usuario
            user = form.save()
            login(self.request, user)
            return super().form_valid(form)
        except IntegrityError:
            # Si hay un error de integridad (username duplicado), agrega un mensaje de error al formulario
            form.add_error('username', 'Este nombre de usuario no está disponible. Por favor, elige otro.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Agrega un mensaje de error al contexto antes de renderizar el template
        error_messages = form.errors
        return render(self.request, self.template_name, {'form': form, 'error_messages': error_messages})

class RegistroOkTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'user/registrook.html'

class LoginView(LoginView):
    template_name = 'user/login.html'

class SalirView(LoginRequiredMixin, LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('auth:login'))


