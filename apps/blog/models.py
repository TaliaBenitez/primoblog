from django.db import models

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from apps.users.models import Perfil

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Receta.Status.PUBLISHED)

# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('nombre',) 

    def __str__(self):
        return self.nombre
    

    
class Receta(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    plato = models.CharField(max_length=255, unique=True)
    url = models.SlugField(max_length=255, unique=True)
    intro = RichTextField()
    ingredientes = RichTextField()
    preparacion = RichTextField()
    vistas = models.PositiveIntegerField(default=0)
    destacada = models.BooleanField(default=False)

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to='receta/imagenes/')
    
    #visible = models.BooleanField(default=True)

    class Status(models.TextChoices):
    
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    objects = models.Manager()
    published = PublishManager()

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


