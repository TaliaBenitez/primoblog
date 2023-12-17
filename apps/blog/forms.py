from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Comentario, Receta, Categoria


class CrearComentarioForm(forms.ModelForm):

    comentario = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comentario
        fields = ('user', 'perfil', 'receta', 'comentario')


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['plato', 'intro', 'preparacion', 'destacada', 'categoria',
                  'status', 'imagen']

    plato = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )
    intro = forms.CharField(
        widget=CKEditorWidget(
            attrs={'class': 'form-control'})
    )
    preparacion = forms.CharField(
        widget=CKEditorWidget(
            attrs={'class': 'form-control'})
    )
    destacada = forms.BooleanField(
        widget=forms.CheckboxInput(),
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.BooleanField(
        widget=forms.CheckboxInput()
    )