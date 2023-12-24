from typing import Any
from django.db import models

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from apps.users.models import Perfil

# Creando los modelos

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Receta.Estado.PUBLISHED)

class Contacto(models.Model):
    nombre = models.CharField(max_length=70)
    email = models.EmailField(max_length=50)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('nombre',) 

    def __str__(self):
        return self.nombre
    
    
class Receta(models.Model):
    class Estado(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    status = models.CharField(max_length=2,
                            choices=Estado.choices,
                            default=Estado.DRAFT)
    plato = models.CharField(max_length=255, unique=True)
    url = models.SlugField(max_length=255, unique=True)
    intro = RichTextField()
    preparacion = RichTextField()
    vistas = models.PositiveIntegerField(default=0)
    destacada = models.BooleanField(default=False)

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to='receta/imagenes/')
    
    objects = models.Manager()
    published = PublishManager()
    visible = models.BooleanField(default=True)
    publish = models.DateTimeField(default=timezone.now)
    creado = models.DateTimeField(default=timezone.now)
    modificado = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish']

    def save(self, *args, **kwargs):
        self.url = slugify(self.plato)
        super(Receta, self).save(*args, **kwargs)  
    def __str__(self):
        return f'{self.plato} - {self.user.username}'
    
class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    receta = models.ForeignKey(Receta, on_delete=models.PROTECT)
    comentario = models.CharField(max_length=5000)
    visible = models.BooleanField(default=True)
    creado = models.DateTimeField(default=timezone.now)



