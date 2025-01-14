from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Pedido, UserProfile, UnidadRT, Base
from .forms import PedidoForm, UserForm, UserProfileForm, UnidadRTForm, BaseForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Count
from datetime import datetime
from django.utils.timezone import make_aware
from django.utils.timezone import make_aware
from django.shortcuts import render
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Pedido
from django.core.paginator import Paginator


# Vista para mostrar detalles de un pedido
@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})

from django.shortcuts import render, get_object_or_404
from .models import Pedido

def ver_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)  # Obtener el pedido con el ID dado o mostrar error 404
    return render(request, 'pedidos/ver_pedido.html', {'pedido': pedido})  # Renderizar una plantilla para mostrar el pedido

# Vista para cancelar un pedido
@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '').strip()
        if motivo:
            pedido.cancelado = True
            pedido.motivo_cancelacion = motivo
            pedido.save()
            return redirect('pedidos:lista_pedidos')
        else:
            error_message = "Debe proporcionar un motivo para cancelar el pedido."
            return render(request, 'pedidos/cancelar_pedido.html', {'pedido': pedido, 'error_message': error_message})

    return render(request, 'pedidos/cancelar_pedido.html', {'pedido': pedido})
# Formulario para cancelar un pedido
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Pedido
from django.utils import timezone
from django.db.models import Q

def ver_pedidos_por_usuario(request, usuario_id):
    # Obtener el usuario operador seleccionado
    usuario = User.objects.get(id=usuario_id)
    
    # Obtener todos los pedidos de ese usuario
    pedidos = Pedido.objects.filter(usuario=usuario)

    # Filtrar por rango de fechas si se proporcionan
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(fecha_hora_pedido__range=[fecha_inicio, fecha_fin])

    return render(request, 'pedidos/usuario.html', {
        'usuario': usuario,
        'pedidos': pedidos,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })
def seleccionar_operador(request):
    # Obtener a los usuarios operadores
    operadores = User.objects.filter(userprofile__rango='Operador')
    return render(request, 'pedidos/seleccionar_operador.html', {'operadores': operadores})

# Vista para listar pedidos con paginación y filtro
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Pedido
from django.core.paginator import Paginator

@login_required  # Decorador correctamente ubicado
def lista_pedidos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        fecha_inicio_dt = make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'))
        fecha_fin_dt = make_aware(datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))
        pedidos = Pedido.objects.filter(fecha_hora_pedido__range=(fecha_inicio_dt, fecha_fin_dt))
    else:
        pedidos = Pedido.objects.all().order_by('-fecha_hora_pedido')


    paginator = Paginator(pedidos, 50)  # Mostrar 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pedidos/lista_pedidos.html', {
        'page_obj': page_obj,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

#
@login_required  # Decorador correctamente ubicado
def lista_general_de_pedidos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        fecha_inicio_dt = make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'))
        fecha_fin_dt = make_aware(datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))
        pedidos = Pedido.objects.filter(fecha_hora_pedido__range=(fecha_inicio_dt, fecha_fin_dt))
    else:
        pedidos = Pedido.objects.all().order_by('-fecha_hora_pedido')


    paginator = Paginator(pedidos, 50)  # Mostrar 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pedidos/lista_general_de_pedidos.html',  {
        'page_obj': page_obj,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

#
from django.utils.timezone import make_aware
from datetime import datetime, timezone
from django.shortcuts import render
from .models import Pedido

def lista_pedidos_general(request):
    # Obtener los parámetros del filtro
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Depuración: Ver los valores de fecha antes de hacer nada
    print(f"Fecha inicio recibida: {fecha_inicio}")
    print(f"Fecha fin recibida: {fecha_fin}")

    # Obtener todos los pedidos por defecto
    pedidos = Pedido.objects.all().order_by('-fecha_hora_pedido')
    print(f"Pedidos obtenidos sin filtro: {pedidos.count()}")  # Depuración: Cantidad de pedidos sin filtros

    # Filtrar por fecha si las fechas están presentes
    if fecha_inicio and fecha_fin:
        try:
            print("Aplicando filtro de fecha...")

            # Convertir las fechas a UTC
            fecha_inicio_dt = make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'), timezone=timezone.utc)
            fecha_fin_dt = make_aware(datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'), timezone=timezone.utc)

            # Depuración: Ver fechas después de la conversión
            print(f"Fecha inicio convertida a UTC: {fecha_inicio_dt}")
            print(f"Fecha fin convertida a UTC: {fecha_fin_dt}")

            # Filtrar los pedidos en el rango de fechas
            pedidos = pedidos.filter(fecha_hora_pedido__range=(fecha_inicio_dt, fecha_fin_dt))
            print(f"Pedidos después de filtrar por fecha: {pedidos.count()}")  # Depuración: Cantidad de pedidos filtrados por fecha

        except Exception as e:
            print(f"Error al filtrar por fecha: {e}")

    # Enviar directamente los pedidos a la plantilla
    return render(request, 'pedidos/lista_pedidos_general.html', {
        'pedidos': pedidos,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


# Vista para eliminar un pedido
@login_required
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidos:lista_pedidos')
    return render(request, 'pedidos/eliminar_pedido.html', {'pedido': pedido})
# Vista para eliminar un pedidos
@login_required
def eliminar_pedidos(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidos:lista_general_de_pedidos')
    return render(request, 'pedidos/eliminar_pedidos.html', {'pedido': pedido})

# Vista para editar un pedido
@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidos:lista_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/editar_pedido.html', {'form': form, 'pedido': pedido})
# Vista para editar un pedido
# Vista para editar un pedido
@login_required
def editar_pedido_general_de_lista(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidos:lista_general_de_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/editar_pedido_general_de_lista.html', {'form': form, 'pedido': pedido})

# Vista para crear un nuevo pedido
from django.db.models import IntegerField, Value, Case, When
from django.db.models.functions import Cast, Substr, Length

@login_required
def nuevo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            if not pedido.fecha_hora_pedido:
                pedido.fecha_hora_pedido = timezone.now()
            pedido.save()
            return redirect('pedidos:nuevo_pedido')
    else:
        form = PedidoForm()

    # Filtrar y ordenar unidades activas
    unidades_activas = UnidadRT.objects.filter(estado='activo').annotate(
        # Extraemos la parte alfabética
        parte_alfabetica=Substr('nombre', 1, Length('nombre') - 2),  # Extraemos lo que no sea numérico al final
        # Extraemos la parte numérica si existe
        parte_numerica=Case(
            When(nombre__regex=r'\d+$', then=Cast(Substr('nombre', Length('nombre') - 1), IntegerField())),  # Solo convierte si hay número
            default=Value(0),
            output_field=IntegerField()
        )
    ).order_by('parte_alfabetica', 'parte_numerica')  # Ordenamos primero alfabéticamente, luego por número

    form.fields['unidad_rt'].queryset = unidades_activas  # Asigna el queryset filtrado y ordenado al campo del formulario

    return render(request, 'pedidos/nuevo_pedido.html', {'form': form})

# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('menu')
    else:
        form = AuthenticationForm()
    return render(request, 'pedidos/login.html', {'form': form})

# Vista del menú dependiendo del usuario
@login_required
def menu_view(request):
    if request.user.is_superuser:
        return redirect('pedidos:menu_admin')
    return redirect('pedidos:menu_operador')

# Vista del menú del operador
@login_required
def menu_operador(request):
    try:
        perfil = UserProfile.objects.get(user=request.user)
        nombre_completo = perfil.nombre_completo or request.user.get_full_name()
        turno = perfil.turno or 'Sin turno asignado'
    except UserProfile.DoesNotExist:
        nombre_completo = request.user.get_full_name()
        turno = 'Sin turno asignado'

    context = {
        'nombre_completo': nombre_completo,
        'turno': turno
    }
    return render(request, 'menu_operador.html', context)

# Vista del menú del administrador
@login_required
def menu_admin(request):
    try:
        perfil = UserProfile.objects.get(user=request.user)
        turno = perfil.turno or 'Sin turno asignado'
        nombre_completo = perfil.nombre_completo or request.user.get_full_name()
    except UserProfile.DoesNotExist:
        turno = 'Sin turno asignado'
        nombre_completo = request.user.get_full_name()

    context = {
        'nombre_completo': nombre_completo,
        'turno': turno
    }
    return render(request, 'menu_admin.html', context)

# Vista para crear un nuevo usuario
@login_required
def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('lista_usuarios')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'create_user.html', {'user_form': user_form, 'profile_form': profile_form})

# Vista para generar el reporte del día
@login_required
def generar_reporte_dia(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))

        pedidos = Pedido.objects.filter(fecha_hora_pedido__range=(fecha_inicio, fecha_fin)).order_by('operador', 'turno')

        # Agrupar por operador y turno
        operadores_turnos = {}
        for pedido in pedidos:
            clave = (pedido.operador, pedido.turno)
            if clave not in operadores_turnos:
                operadores_turnos[clave] = []
            operadores_turnos[clave].append(pedido)

        # Resumen General
        total_pedidos = pedidos.count()
        total_unidades_movilizadas = pedidos.values('unidad_rt').distinct().count()
        total_bases_movilizadas = pedidos.values('base').distinct().count()
        total_llamadas = pedidos.values('telefono').distinct().count()
        total_pedidos_cancelados = pedidos.filter(cancelado=True).count()

        unidades_mas_solicitadas = pedidos.values('unidad_rt__nombre').annotate(count=Count('unidad_rt')).order_by('-count')
        unidad_rt_mas_solicitada = unidades_mas_solicitadas.first()
        bases_mas_solicitadas = pedidos.values('base__nombre').annotate(count=Count('base')).order_by('-count')
        base_mas_solicitada = bases_mas_solicitadas.first()

        telefonos_mas_solicitados = pedidos.values('telefono').annotate(count=Count('telefono')).order_by('-count')
        telefono_mas_solicitado = telefonos_mas_solicitados.first()

        template_path = 'pedidos/reporte_dia_pdf.html'
        context = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'operadores_turnos': operadores_turnos,
            'total_pedidos': total_pedidos,
            'total_unidades_movilizadas': total_unidades_movilizadas,
            'total_bases_movilizadas': total_bases_movilizadas,
            'total_llamadas': total_llamadas,
            'total_pedidos_cancelados': total_pedidos_cancelados,
            'unidad_rt_mas_solicitada': unidad_rt_mas_solicitada,
            'base_mas_solicitada': base_mas_solicitada,
            'telefono_mas_solicitado': telefono_mas_solicitado,
        }
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_dia.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Hubo un error al generar el PDF')
        return response

    return render(request, 'pedidos/generar_reporte_dia.html')

# Vista para listar Unidades RT y Bases
from django.db.models import IntegerField, Value, Case, When
from django.db.models.functions import Cast, Substr

@login_required
def unidades_bases(request):
    unidades_rt = UnidadRT.objects.annotate(
        numero=Case(
            When(nombre__startswith='rt ', then=Cast(Substr('nombre', 4), IntegerField())),  # Solo extrae y convierte si empieza con 'rt '
            default=Value(0),  # Asigna 0 a las unidades que no tienen número
            output_field=IntegerField()
        )
    ).order_by('numero')

    bases = Base.objects.all()
    return render(request, 'pedidos/unidades_bases.html', {'unidades_rt': unidades_rt, 'bases': bases})

# Vista para agregar una nueva Unidad RT
@login_required
def agregar_unidad_rt(request):
    if request.method == 'POST':
        form = UnidadRTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos:unidades_bases')
    else:
        form = UnidadRTForm()
    return render(request, 'pedidos/agregar_unidad_rt.html', {'form': form})

# Vista para editar una Unidad RT existente
@login_required
def editar_unidad_rt(request, pk):
    unidad = get_object_or_404(UnidadRT, pk=pk)
    if request.method == 'POST':
        form = UnidadRTForm(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect('pedidos:unidades_bases')
    else:
        form = UnidadRTForm(instance=unidad)
    return render(request, 'pedidos/editar_unidad_rt.html', {'form': form})

# Vista para eliminar una Unidad RT
@login_required
def eliminar_unidad_rt(request, pk):
    unidad = get_object_or_404(UnidadRT, pk=pk)
    if request.method == 'POST':
        unidad.delete()
        return redirect('pedidos:unidades_bases')
    return render(request, 'pedidos/eliminar_unidad_rt.html', {'unidad': unidad})

# Vista para agregar una nueva Base
@login_required
def agregar_base(request):
    if request.method == 'POST':
        form = BaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos:unidades_bases')
    else:
        form = BaseForm()
    return render(request, 'pedidos/agregar_base.html', {'form': form})

# Vista para editar una Base existente
@login_required
def editar_base(request, pk):
    base = get_object_or_404(Base, pk=pk)
    if request.method == 'POST':
        form = BaseForm(request.POST, instance=base)
        if form.is_valid():
            form.save()
            return redirect('pedidos:unidades_bases')
    else:
        form = BaseForm(instance=base)
    return render(request, 'pedidos/editar_base.html', {'form': form})

# Vista para eliminar una Base
@login_required
def eliminar_base(request, pk):
    base = get_object_or_404(Base, pk=pk)
    if request.method == 'POST':
        base.delete()
        return redirect('pedidos:unidades_bases')
    return render(request, 'pedidos/eliminar_base.html', {'base': base})

# Vista para listar Usuarios Operadores
@login_required
def usuarios_vistas(request):
    # Filtra correctamente los usuarios que tienen el rango de 'Operador'
    usuarios = UserProfile.objects.filter(rango='Operador')
    return render(request, 'pedidos/usuarios_vistas.html', {'usuarios': usuarios})
# Vista para generar el reporte del día
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render
from .models import Pedido
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from .models import Pedido
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import ReporteDiaForm

# Vista para generar el reporte del día
def reporte_del_dia(request):
    if request.method == 'POST':
        form = ReporteDiaForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            # Filtrar pedidos por el rango de fechas
            pedidos = Pedido.objects.filter(fecha_hora_pedido__range=(fecha_inicio, fecha_fin))

            # Resumen general
            total_pedidos = pedidos.count()
            total_unidades_movilizadas = pedidos.values('unidad_rt').distinct().count()
            total_bases_movilizadas = pedidos.values('base').distinct().count()
            total_llamadas = pedidos.values('telefono').distinct().count()
            total_pedidos_cancelados = pedidos.filter(cancelado=True).count()

            # Cálculos adicionales
            unidad_rt_mas_solicitada = pedidos.values('unidad_rt__nombre').annotate(count=Count('unidad_rt')).order_by('-count').first()
            base_mas_solicitada = pedidos.values('base__nombre').annotate(count=Count('base')).order_by('-count').first()
            telefono_mas_solicitado = pedidos.values('telefono').annotate(count=Count('telefono')).order_by('-count').first()

            # Para cada pedido, obten el perfil del usuario asociado y el turno
            pedidos_con_perfiles = []
            for pedido in pedidos:
                perfil_usuario = UserProfile.objects.get(user=pedido.usuario)  # Obtenemos el perfil del usuario
                pedidos_con_perfiles.append({
                    'pedido': pedido,
                    'nombre_operador': perfil_usuario.nombre_completo,
                    'turno': perfil_usuario.turno
                })

            # Generar el PDF
            template_path = 'pedidos/reporte_dia_pdf.html'
            context = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'total_pedidos': total_pedidos,
                'total_unidades_movilizadas': total_unidades_movilizadas,
                'total_bases_movilizadas': total_bases_movilizadas,
                'total_llamadas': total_llamadas,
                'total_pedidos_cancelados': total_pedidos_cancelados,
                'unidad_rt_mas_solicitada': unidad_rt_mas_solicitada,
                'base_mas_solicitada': base_mas_solicitada,
                'telefono_mas_solicitado': telefono_mas_solicitado,
                'pedidos_con_perfiles': pedidos_con_perfiles,  # Enviamos los pedidos con perfiles
            }
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="reporte_dia.pdf"'
            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('Hubo un error al generar el PDF')
            return response

    else:
        form = ReporteDiaForm()

    return render(request, 'pedidos/generar_reporte_dia.html', {'form': form})

# Vista para agregar un nuevo Usuario Operador
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm
from .models import UserProfile

@login_required
def agregar_usuario(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Guardar el nuevo usuario sin guardar todavía la contraseña
            user = user_form.save(commit=False)

            # Asignar la contraseña ingresada en el formulario
            user.set_password(user_form.cleaned_data['password'])
            
            # Guardar el usuario con la contraseña encriptada
            user.save()

            # Crear o actualizar el perfil de usuario
            profile, created = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'nombre_completo': profile_form.cleaned_data.get('nombre_completo'),
                    'turno': profile_form.cleaned_data.get('turno'),
                    'rango': profile_form.cleaned_data.get('rango')
                }
            )
            return redirect('pedidos:usuarios_vistas')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'pedidos/agregar_usuario.html', {'user_form': user_form, 'profile_form': profile_form})

# Vista para editar un Usuario Operador existente
from django.shortcuts import get_object_or_404, redirect
from .models import UserProfile
from .forms import UserForm, UserProfileForm

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=usuario.user)
        profile_form = UserProfileForm(request.POST, instance=usuario)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('pedidos:usuarios_vistas')
    else:
        user_form = UserForm(instance=usuario.user)
        profile_form = UserProfileForm(instance=usuario)
    return render(request, 'pedidos/editar_usuario.html', {'user_form': user_form, 'profile_form': profile_form})

# Vista para eliminar un Usuario Operador
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('pedidos:usuarios_vistas')
    return render(request, 'pedidos/eliminar_usuario.html', {'usuario': usuario})

# Vista para listar pedidos por usuario
@login_required
def pedidos_por_usuario(request):
    usuario_actual = request.user
    pedidos = Pedido.objects.filter(operador=usuario_actual)
    return render(request, 'pedidos/pedidos_por_usuario.html', {'pedidos': pedidos})

# Vista para lista de pedidos general
@login_required
def lista_pedidos_general(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista_pedidos_general.html', {'pedidos': pedidos})
@login_required
def redirigir_usuario(request):
    if request.user.is_superuser:
        return redirect('menu_admin')  # Ajusta a la vista o URL correspondiente
    else:
        return redirect('menu_operador')  # Ajusta a la vista o URL correspondiente
 #Generar reporte del dia
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import ReporteDiaForm
from .models import Pedido, UserProfile
from django.db.models import Count
from django.db.models import Count, Avg

from django.db.models import Count, Avg
from datetime import timedelta

def generar_reporte_dia(request):
    if request.method == 'POST':
        form = ReporteDiaForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            fecha_fin = form.cleaned_data.get('fecha_fin')

            if fecha_inicio is None or fecha_fin is None:
                return HttpResponse('Las fechas no pueden estar vacías.', status=400)

            # Filtrar los pedidos
            pedidos = Pedido.objects.filter(
                fecha_hora_pedido__range=(fecha_inicio, fecha_fin)
            ).order_by('usuario__userprofile__nombre_completo', 'usuario__userprofile__turno')

            # Agrupar pedidos por operador y turno
            resumen_por_operador = {}
            for pedido in pedidos:
                operador = f"{pedido.usuario.userprofile.nombre_completo} ({pedido.usuario.userprofile.turno})"
                if operador not in resumen_por_operador:
                    resumen_por_operador[operador] = {
                        'total_pedidos': 0,
                        'total_cancelados': 0,
                        'pedidos': []
                    }
                resumen_por_operador[operador]['total_pedidos'] += 1
                if pedido.cancelado:
                    resumen_por_operador[operador]['total_cancelados'] += 1
                resumen_por_operador[operador]['pedidos'].append(pedido)

            # Resumen general
            total_pedidos = pedidos.count()
            total_unidades_movilizadas = pedidos.values('unidad_rt').distinct().count()
            total_bases_movilizadas = pedidos.values('base').distinct().count()
            total_llamadas = pedidos.values('telefono').distinct().count()
            total_pedidos_cancelados = pedidos.filter(cancelado=True).count()
            pedidos_cancelados = pedidos.filter(cancelado=True)

            # Cálculos adicionales
            unidad_rt_mas_solicitada = pedidos.values('unidad_rt__nombre').annotate(count=Count('unidad_rt')).order_by('-count').first()
            base_mas_solicitada = pedidos.values('base__nombre').annotate(count=Count('base')).order_by('-count').first()
            telefono_mas_solicitado = pedidos.values('telefono__nombre').annotate(count=Count('telefono')).order_by('-count').first()

            # Promedio de viajes por hora
            horas_diferencia = (fecha_fin - fecha_inicio).total_seconds() / 3600
            promedio_viajes_hora = total_pedidos / horas_diferencia if horas_diferencia > 0 else 0

            # Lista de teléfonos con su total de llamadas
            telefonos_llamadas = pedidos.values('telefono__nombre').annotate(total_llamadas=Count('telefono')).order_by('-total_llamadas')

            # Unidades RT con más de 5 viajes
            unidades_rt_mas_de_5_viajess = pedidos.values('unidad_rt__nombre').annotate(total_viajes=Count('unidad_rt')).filter(total_viajes__gt=5)

            # Unidades RT y su total de viajes
            unidades_rt_viajes = pedidos.values('unidad_rt__nombre').annotate(total_viajes=Count('unidad_rt')).order_by('-total_viajes')

            # Total de viajes cancelados por unidad RT
            viajes_cancelados = pedidos.filter(cancelado=True).values('unidad_rt__nombre').annotate(total_cancelados=Count('unidad_rt')).order_by('-total_cancelados')
           
            # Desglose de viajes cancelados por cliente y otros motivos
            cancelados_por_cliente = pedidos_cancelados.filter(motivo_cancelacion='cliente').count()
            cancelados_por_otros = pedidos_cancelados.exclude(motivo_cancelacion='cliente').count()

            # Crear el contexto para el PDF
            context = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'resumen_por_operador': resumen_por_operador,
                'total_pedidos': total_pedidos,
                'total_unidades_movilizadas': total_unidades_movilizadas,
                'total_bases_movilizadas': total_bases_movilizadas,
                'total_llamadas': total_llamadas,
                'total_pedidos_cancelados': total_pedidos_cancelados,
                'unidad_rt_mas_solicitada': unidad_rt_mas_solicitada,
                'base_mas_solicitada': base_mas_solicitada,
                'telefono_mas_solicitado': telefono_mas_solicitado,
                'promedio_viajes_hora': promedio_viajes_hora,
                'telefonos_llamadas': telefonos_llamadas,
                'unidades_rt_mas_de_5_viajess': unidades_rt_mas_de_5_viajess,
                'unidades_rt_viajes': unidades_rt_viajes,
                'viajes_cancelados': viajes_cancelados,
                'cancelados_por_cliente': cancelados_por_cliente,
                'cancelados_por_otros': cancelados_por_otros,
            }
            
            # Generar el PDF
            template_path = 'pedidos/reporte_dia_pdf.html'
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="reporte_dia.pdf"'
            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('Hubo un error al generar el PDF', status=500)
            return response
        else:
            return HttpResponse('El formulario no es válido. Asegúrate de que los campos estén correctos.', status=400)
    else:
        form = ReporteDiaForm()

    return render(request, 'pedidos/generar_reporte_dia.html', {'form': form})

#generar_reporte_turno
@login_required
def generar_reporte_turno(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))

        pedidos = Pedido.objects.filter(fecha_hora_pedido__range=(fecha_inicio, fecha_fin))

        total_pedidos = pedidos.count()
        pedidos_cancelados = pedidos.filter(cancelado=True)
        pedidos_activos = pedidos.filter(cancelado=False)
        total_unidades_movilizadas = pedidos.values('unidad_rt').distinct().count()

        # Unidad RT más solicitada
        unidad_rt_mas_solicitada = pedidos.values('unidad_rt__nombre').annotate(count=Count('unidad_rt')).order_by('-count').first()

        # Base más solicitada
        base_mas_solicitada = pedidos.values('base__nombre').annotate(count=Count('base')).order_by('-count').first()

        # Promedio de viajes por unidad RT
        promedio_viajes_por_unidad = pedidos.values('unidad_rt').annotate(promedio=Count('unidad_rt')).count()

        # Promedio de viajes por base
        promedio_viajes_por_base = pedidos.values('base').annotate(promedio=Count('base')).count()

        # Desglose de viajes cancelados por cliente y otros motivos
        cancelados_por_cliente = pedidos_cancelados.filter(motivo_cancelacion='cliente').count()
        cancelados_por_otros = pedidos_cancelados.exclude(motivo_cancelacion='cliente').count()

        # Unidades RT con más de cinco viajes
        unidades_con_mas_de_cinco_viajes = pedidos.values('unidad_rt__nombre').annotate(count=Count('unidad_rt')).filter(count__gt=5)
        
        # Teléfono más solicitado
        telefono_mas_solicitado = pedidos.values('telefono').annotate(count=Count('telefono')).order_by('-count').first()

        # Los cuatro teléfonos más utilizados
        telefonos_top = pedidos.values('telefono').annotate(count=Count('telefono')).order_by('-count')[:4]
        # Teléfono más solicitado
        telefono = {
            '5558808251': pedidos.filter(telefono='5558808251').count(),
            '5558178115': pedidos.filter(telefono='5558178115').count(),
            '5563066325': pedidos.filter(telefono='5563066325').count(),
            '5551527971': pedidos.filter(telefono='5551527971').count(),
        }
        tel_mas_solicitado = max(telefono, key=telefono.get)

        # Teléfonos con más de cinco llamadas
        telefonos_con_mas_de_cinco_llamadas = pedidos.values('telefono').annotate(count=Count('telefono')).filter(count__gt=5)

        # Obtener datos del usuario que inició sesión
        user = request.user
        user_profile = user.userprofile  # Asumiendo que tienes un modelo UserProfile asociado

        # Generar PDF
        template_path = 'pedidos/reporte_turno_pdf.html'
        context = {
            'user': user,
            'turno': user_profile.turno,
            'pedidos': pedidos,
            'total_pedidos': total_pedidos,
            'total_unidades_movilizadas': total_unidades_movilizadas,
            'unidad_rt_mas_solicitada': unidad_rt_mas_solicitada,
            'base_mas_solicitada': base_mas_solicitada,
            'promedio_viajes_por_unidad': promedio_viajes_por_unidad,
            'promedio_viajes_por_base': promedio_viajes_por_base,
            'cancelados_por_cliente': cancelados_por_cliente,
            'cancelados_por_otros': cancelados_por_otros,
            'pedidos_activos': pedidos_activos,
            'unidades_con_mas_de_cinco_viajes': unidades_con_mas_de_cinco_viajes,
            'pedidos_cancelados': pedidos_cancelados,
            'telefono_mas_solicitado': telefono_mas_solicitado,
            'tel_mas_solicitado': tel_mas_solicitado,
            'telefonos_con_mas_de_cinco_llamadas': telefonos_con_mas_de_cinco_llamadas,
            'telefonos_top': telefonos_top,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
            
            
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_turno.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Hubo un error al generar el PDF')
        return response

    return render(request, 'pedidos/generar_reporte_turno.html')