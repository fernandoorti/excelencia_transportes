from django import forms
from django.utils.timezone import now
from .models import Pedido, Telefono, UnidadRT, Base, UserProfile
from django.contrib.auth.models import User

# Formulario para crear y editar pedidos
class PedidoForm(forms.ModelForm):
    telefono = forms.ModelChoiceField(
        queryset=Telefono.objects.all(),
        empty_label="Selecciona un número de teléfono",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    unidad_rt = forms.ModelChoiceField(
        queryset=UnidadRT.objects.filter(estado='activo'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_hora_pedido = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Pedido
        fields = ['cliente', 'ubicacion_cliente', 'destino', 'unidad_rt', 'base', 'telefono', 'fecha_hora_pedido', 'cancelado', 'observacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_fecha_hora_pedido(self):
        return self.cleaned_data.get('fecha_hora_pedido') or now()

# Formulario para crear y editar usuarios
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Nueva Contraseña", required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Nueva Contraseña", required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if password := self.cleaned_data.get('password'):
            user.set_password(password)
        if commit:
            user.save()
        return user

# Formulario para gestionar perfiles de usuario
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nombre_completo', 'turno', 'rango']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'rango': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para gestionar Unidades RT
class UnidadRTForm(forms.ModelForm):
    class Meta:
        model = UnidadRT
        fields = ['nombre', 'estado', 'nombre_operador']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'nombre_operador': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para gestionar Bases
class BaseForm(forms.ModelForm):
    class Meta:
        model = Base
        fields = ['nombre', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para generar reportes
class ReporteDiaForm(forms.Form):
    fecha_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Fecha de inicio'
    )
    fecha_fin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Fecha de fin'
    )

# Formulario para filtrar pedidos
class FiltroPedidosForm(forms.Form):
    fecha_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=False, label='Fecha de inicio'
    )
    fecha_fin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=False, label='Fecha de fin'
    )

# Formulario para filtrar pedidos por usuario y fecha
class FiltroPedidosUsuarioForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(rango__iexact='Operador'),
        required=False,
        label='Usuario Operador',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=False, label='Fecha de inicio'
    )
    fecha_fin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=False, label='Fecha de fin'
    )
