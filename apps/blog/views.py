import os
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Receta, Categoria, Comentario, Contacto
from .forms import CrearComentarioForm, RecetaForm, ContactoForm


class RecetaCreateView(UserPassesTestMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'blog/receta/crear_receta.html'
    success_url = reverse_lazy('blog:inicio')
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Administrador', 'Colaborador']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.perfil = self.request.user.perfil
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Agregar Receta'
        return context
    
class RecetaUpdateView(UserPassesTestMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'blog/receta/crear_receta.html'
    slug_field = 'url'
    slug_url_kwarg = 'url'
    success_url = reverse_lazy('blog:inicio')
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Administrador']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) or self.request.user == self.get_object().user

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.perfil = self.request.user.perfil
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Actualizar Receta'
        return context
    
class RecetaDeleteView(UserPassesTestMixin, DeleteView):
    model = Receta
    slug_field = 'url'
    slug_url_kwarg = 'url'
    success_url = reverse_lazy('blog:inicio')
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Administrador']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) or self.request.user == self.get_object().user

    def form_valid(self, form):
        # Obtener  objeto Receta
        receta = self.get_object()

        # Eliminar  imagen asociada
        if receta.imagen:
            # Obtener ruta completa del archivo de imagen
            image_path = receta.imagen.path

            # Verificar si el archivo existe y eliminarlo
            if os.path.exists(image_path):
                os.remove(image_path)

        return super().form_valid(form)
    

    


class InicioListView(ListView):
    model = Receta
    template_name = 'blog/index.html'
    context_object_name = 'recetas'
    paginate_by = 2
    ordering = ['-publish']
    queryset = Receta.objects.filter(visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['recetas_destacadas'] = Receta.objects.filter(
            destacada=True, visible=True)
        return context
    

    
class NosotrosTemplateView(TemplateView):
    template_name = 'blog/nosotros.html'


class ContactoFormView(FormView):
    form_class = ContactoForm
    template_name = 'blog/contacto.html'
    success_url = reverse_lazy('blog:contactook')


class ContactoTemplateView(TemplateView):
    template_name = 'blog/contacto.html'


class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'blog/detalle.html'
    context_object_name = 'receta'
    slug_field = 'url'
    slug_url_kwarg = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recetas'] = Receta.objects.filter(visible=True)
        context['categorias'] = Categoria.objects.all()
        context['comentarios'] = Comentario.objects.filter(
            visible=True, receta=self.get_object()).all()
        context['cantidad_comentarios'] = Comentario.objects.filter(
            visible=True, receta=self.get_object()).all().count()
        return context
    
class ComentarioView(UserPassesTestMixin, View):
    template_name = 'blog/detalle.html'
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Colaborador', 'Administrador', 'Registrado']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=group).exists() for group in grupos)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=405)

    def post(self, request, *args, **kwargs):
        url = request.POST.get('url')
        receta = {
            'user': request.user.id,
            'perfil': request.user.perfil.id,
            'comentario': request.POST.get('comentario'),
            'receta': request.POST.get('receta')
        }
        form = CrearComentarioForm(receta)
        if form.is_valid():
            form.save()
            return redirect('blog:detalle', url=url)
        else:
            return HttpResponse(status=500)


class CategoriaListView(ListView):
    model = Receta
    template_name = 'blog/index.html'
    context_object_name = 'recetas'
    paginate_by = 2
    ordering = ['-publish']

    def get_queryset(self):
        receta = None
        if self.kwargs['categoria_id']:
            categoria_id = self.kwargs['categoria_id']
            categoria = Categoria.objects.filter(id=categoria_id)[:1]
            receta = Receta.objects.filter(categoria=categoria, status='PB')
        return receta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['recetas_destacadas'] = Receta.objects.filter(
            destacada=True, status='PB')
        return context


class UserListView(ListView):
    model = Receta
    template_name = 'blog/index.html'
    context_object_name = 'recetas'
    paginate_by = 2
    ordering = ['-publish']

    def get_queryset(self):
        receta = None
        if self.kwargs['nombre']:
            user_nombre = self.kwargs['nombre']
            user = User.objects.filter(username=user_nombre)[:1]
            receta = Receta.objects.filter(user=user, status='PB')
        return receta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['recetas_destacadas'] = Receta.objects.filter(
            destacada=True, status='PB')
        return context
    
