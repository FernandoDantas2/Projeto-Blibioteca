from django.urls import path
from . import views as menu_views

urlpatterns = [
    path('Login_gerente/', menu_views.Login_gerente, name='Login_gerente'),
    path('Logout_gerente/', menu_views.Logout_gerente, name='Logout_gerente'),
    path('Listar_solicitacoes/', menu_views.Listar_solicitacoes, name='Listar_solicitacoes'),
    path('Cadastro_funcionario/', menu_views.Cadastro_funcionario, name='Cadastro_funcionario'),
    path('Aprovar_solicitacao/',menu_views.Aprovar_solicitacao, name='Aprovar_solicitacao'),
    path('Login_funcionario/', menu_views.Login_funcionario,name='Login_funcionario'),
    path('Logout_funcionario/', menu_views.Logout_funcionario,name='Logout_funcionario'),
    path('Excluir_funcionario/', menu_views.Excluir_funcionario, name='Excluir_funcionario'),
    path('Cadastra_usuario/', menu_views.Cadastra_usuario,name='Cadastrar_usuario'),
    path('Cadastra_livro/', menu_views.Cadastra_livro, name='Cadastra_livro'),
    path('Listar_livros/', menu_views.Listar_livros, name='Listar_livros'),
    path('Renovar_emprestimo/', menu_views.Renovar_emprestimo, name='Renovar_emprestimo'),
    path('Liberar_emprestimo/', menu_views.Liberar_emprestimo, name='Liberar_emprestimo'),
    path('Cancelar_emprestimo/', menu_views.Cancelar_emprestimo, name='Cancelar_emprestimo'),
    path('', menu_views.Home, name='Home'),
    path('Excluir_livro/', menu_views.Excluir_livro, name='Excluir_livro'),
]