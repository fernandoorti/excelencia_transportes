from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),

    path('lista-general/', views.lista_general_de_pedidos, name='lista_general_de_pedidos'),
    path('<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),

    path('pedidos/seleccionar-operador/', views.seleccionar_operador, name='seleccionar_operador'),
    path('pedidos/ver-pedidos-por-usuario/<int:usuario_id>/', views.ver_pedidos_por_usuario, name='ver_pedidos_por_usuario'),

    path('pedido/<int:id>/', views.ver_pedido, name='ver_pedido'),  # Definir la ruta para ver un pedido
    path('<int:pedido_id>/eliminar_pedidos/', views.eliminar_pedidos, name='eliminar_pedidos'),
    
    path('<int:pedido_id>/editar_pedidos/', views.editar_pedido_general_de_lista, name='editar_pedido_general'),
  
    path('nuevo/', views.nuevo_pedido, name='nuevo_pedido'),

    path('menu/', views.menu_view, name='menu'),
    path('<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('<int:pedido_id>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),
    path('<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
    path('redirigir/', views.redirigir_usuario, name='redirigir_usuario'),
    path('reporte_del_dia/', views.reporte_del_dia, name='reporte_del_dia'),
    path('reporte_del_dia/', views.reporte_del_dia, name='reporte_del_dia'),
    
    path('menu_operador/', views.menu_operador, name='menu_operador'),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('unidades_bases/', views.unidades_bases, name='unidades_bases'),
    path('agregar_unidad_rt/', views.agregar_unidad_rt, name='agregar_unidad_rt'),
    path('unidades_rt/editar/<int:pk>/', views.editar_unidad_rt, name='editar_unidad_rt'),
    path('unidades_rt/eliminar/<int:pk>/', views.eliminar_unidad_rt, name='eliminar_unidad_rt'),
    path('bases/agregar/', views.agregar_base, name='agregar_base'),
    path('bases/editar/<int:pk>/', views.editar_base, name='editar_base'),
    path('bases/eliminar/<int:pk>/', views.eliminar_base, name='eliminar_base'),
    path('generar_reporte_dia/', views.generar_reporte_dia, name='generar_reporte_dia'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('lista_pedidos_general/', views.lista_pedidos_general, name='lista_pedidos_general'),
    path('usuarios_vistas/', views.usuarios_vistas, name='usuarios_vistas'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('eliminar_usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('reporte_dia.pdf', views.generar_reporte_dia, name='reporte_dia_pdf'),
    path('pedidos_por_usuario/', views.pedidos_por_usuario, name='pedidos_por_usuario'),
    path('generar_reporte_turno/', views.generar_reporte_turno, name='generar_reporte_turno'),
    path('generar_reporte_dia/', views.generar_reporte_dia, name='generar_reporte_dia'),
]
