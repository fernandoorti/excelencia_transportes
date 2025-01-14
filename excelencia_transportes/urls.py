"""
URL configuration for excelencia_transportes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pedidos import views  # Asegúrate de importar tus vistas correctamente
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pedidos/', include('pedidos.urls')),
    path('menu/', views.menu_view, name='menu'),
    path('login/', views.login_view, name='login'),  # Ruta para el login
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),  # Ruta para el logout usando la vista predeterminada
    path('redirigir/', views.redirigir_usuario, name='redirigir_usuario'),  # Redirige según el rol del usuario
    path('', views.login_view, name='home'),  # Página principal (login)
]





