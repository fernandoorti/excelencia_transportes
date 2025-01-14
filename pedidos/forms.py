from django import forms
from django.utils.timezone import now
from .models import Pedido, Telefono, UnidadRT, Base, UserProfile, TURNOS, RANGOS
from django.contrib.auth.models import User

# Formulario para crear y editar pedidos
class PedidoForm(forms.ModelForm):
    telefono = forms.ModelChoiceField(
        queryset=Telefono.objects.all(),
        empty_label="Selecciona un número de teléfono",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Pedido
        fields = ['cliente', 'ubicacion_cliente', 'destino', 'unidad_rt', 'base', 'telefono', 'fecha_hora_pedido', 'cancelado', 'observacion']
    
    # Cambiar unidad_rt a no requerido
    unidad_rt = forms.ModelChoiceField(
        queryset=UnidadRT.objects.filter(estado='activo'),
        required=False  # Esto lo hace opcional
    )
    
 # Redefinir el campo fecha_hora_pedido para usar un widget de tipo datetime-local
    fecha_hora_pedido = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],  # Formato de entrada
    )

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_fecha_hora_pedido(self):
        fecha_hora_pedido = self.cleaned_data.get('fecha_hora_pedido')
        if not fecha_hora_pedido:
            fecha_hora_pedido = now()  # Autocompletar con la fecha y hora actuales si no se proporciona
        return fecha_hora_pedido

# Formulario para crear y editar usuarios del modelo User
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

        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)  # Asignar la nueva contraseña si fue ingresada
        if commit:
            user.save()
        return user
# Formulario para gestionar los perfiles de usuario en UserProfile
TURNOS = (
    ('Mañana', 'Mañana'),
    ('Tarde', 'Tarde'),
    ('Noche', 'Noche'),
)
RANGOS = (
    ('Operador', 'Operador'),
    ('Administrador', 'Administrador'),
)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nombre_completo', 'turno', 'rango']  # Asegúrate de que el campo 'rango' existe en el modelo
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'turno': forms.Select(choices=TURNOS, attrs={'class': 'form-control'}),
            'rango': forms.Select(choices=RANGOS, attrs={'class': 'form-control'}),
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

# Formulario para generar el reporte del día
class ReporteDiaForm(forms.Form):
    fecha_inicio = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), label='Fecha de inicio')
    fecha_fin = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), label='Fecha de fin')

# Formulario para filtrar pedidos por fecha
class FiltroPedidosForm(forms.Form):
    fecha_inicio = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), required=False, label='Fecha de inicio')
    fecha_fin = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), required=False, label='Fecha de fin')

# Formulario para filtrar pedidos por usuario y fecha
class FiltroPedidosUsuarioForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=UserProfile.objects.filter(rango='Operador'), required=False, label='Usuario Operador', widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_inicio = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), required=False, label='Fecha de inicio')
    fecha_fin = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), required=False, label='Fecha de fin')
from django import forms

class ReporteDiaForm(forms.Form):
    fecha_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Fecha de inicio'
    )
    fecha_fin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Fecha de fin'
    )
