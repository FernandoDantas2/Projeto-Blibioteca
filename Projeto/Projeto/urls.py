from django.contrib import admin
from django.urls import path, include
from menuinicial.views import funcionarioViewset, gerenteViewset, UsuarioViewset, LivroViewset, EmprestimoViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('funcionario', funcionarioViewset, basename='funcionario')
router.register('gerente', gerenteViewset, basename='gerente')
router.register('usuario', UsuarioViewset, basename='usuario')  # Corrigido para 'usuario'
router.register('Livro', LivroViewset, basename='Livro')  # Corrigido para 'Livro'
router.register('Emprestimo', EmprestimoViewset, basename='Emprestimo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include(router.urls)),  # Corrigido para fechar corretamente o parêntese
]
