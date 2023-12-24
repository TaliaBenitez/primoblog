from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Comentario, Receta, Categoria, Contacto


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
    visible = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )



class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ('nombre', 'email', 'asunto', 'mensaje')

    nombre = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre y Apellido'}
        )
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'}
        )
    )
    asunto = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Asunto'}
        )
    )
    mensaje = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mensaje'}
        )
    )