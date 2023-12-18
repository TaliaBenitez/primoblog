from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Receta, Categoria, Comentario
from .forms import CrearComentarioForm, RecetaForm


class RecetaCreateView(CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'blog/receta/crear_receta.html'
    success_url = reverse_lazy('blog:inicio')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.perfil = self.request.user.perfil
        return super().form_valid(form)
    
class InicioListView(ListView):
    model = Receta
    template_name = 'blog/index.html'
    context_object_name = 'recetas'
    paginate_by = 2
    ordering = ('-creado',)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['recetas_destacadas'] = Receta.objects.filter(
            destacada=True, visible=True)
        return context
    
class NosotrosTemplateView(TemplateView):
    template_name = 'blog/nosotros.html'


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
            visible=True, auto=self.get_object()).all()
        context['cantidad_comentarios'] = Comentario.objects.filter(
            visible=True, auto=self.get_object()).all().count()
        return context
    
class ComentarioView(UserPassesTestMixin, View):
    template_name = 'blog/detalle.html'

    def test_func(self):
        allowed_groups = ['Colaborador', 'Administrador', 'Registrado']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=group).exists() for group in allowed_groups)

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
            return redirect('bog:detalle', url=url)
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