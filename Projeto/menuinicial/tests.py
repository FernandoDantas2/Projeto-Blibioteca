from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from menuinicial.models import Funcionario, Gerente, Usuario, Livro, Emprestimo, SolicitacaoCadastro
from datetime import datetime, timedelta
from django.utils import timezone


User = get_user_model()
class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.gerente = Gerente.objects.create_user(cpf='12345678900', password='sua_senha', is_gerente=True)
        self.funcionario = Funcionario.objects.create(            
            nome='Nome do Funcionário',
            cpf='12345678900',
            data_nascimento=datetime(1990, 1, 1),
            telefone='123456789',
            endereco='Endereço do Funcionário',
            email='funcionario@example.com',
            password='senha_funcionario'
        )        
        self.funcionario = Funcionario.objects.create(nome='Nome do Funcionário', senha='senha_funcionario')
        self.usuario = Usuario.objects.create()
        self.livro = Livro.objects.create(titulo='Livro Teste', autor='Autor Teste')
        data_devolucao = timezone.now() + timedelta(days=7)
        self.emprestimo = Emprestimo.objects.create(Livro=self.livro, Usuario=self.usuario, Data_devolucao=data_devolucao)

    def test_Login_gerente(self):
        response = self.client.post('/Login_gerente/', {'nome': 'gerente', 'senha': '12345'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Logout_gerente(self):
        self.client.force_login(self.gerente)
        response = self.client.post('/Logout_gerente/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Listar_solicitacoes(self):
        self.client.force_login(self.gerente)
        response = self.client.get('/Listar_solicitacoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Cadastro_funcionario(self):
        self.client.force_login(self.gerente)
        data = {'email': 'funcionario2@example.com', 'nome': 'Funcionário 2', 'cpf': '12345678901', 'data_nascimento': '1990-01-01', 'telefone': '123456789', 'endereco': 'Endereço do Funcionário 2', 'password': 'senha_funcionario'}
        response = self.client.post('/Cadastro_funcionario/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_Aprovar_solicitacao(self):
        funcionario = Funcionario.objects.create(nome='Nome do Funcionário', senha='senha123')
        solicitacao = SolicitacaoCadastro.objects.create(funcionario=funcionario)
        self.client.force_login(self.gerente)
        response = self.client.post(f'/Aprovar_solicitacao/{solicitacao.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Login_funcionario(self):
        response = self.client.post('/Login_funcionario/', {'cpf': '12345678901', 'password': 'sua_senha'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Logout_funcionario(self):
        self.client.force_login(self.funcionario)
        response = self.client.post('/Logout_funcionario/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Excluir_funcionario(self):
        self.client.force_login(self.gerente)
        response = self.client.delete(f'/Excluir_funcionario/{self.funcionario.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_Cadastrar_usuario(self):
        self.client.force_login(self.gerente)
        data = {'username': 'usuario2', 'password': '12345'}
        response = self.client.post('/Cadastrar_usuario/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_Cadastra_livro(self):
        self.client.force_login(self.gerente)
        data = {'titulo': 'Livro Teste 2', 'autor': 'Autor Teste 2'}
        response = self.client.post('/Cadastra_livro/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_Listar_livros(self):
        self.client.force_login(self.funcionario)
        response = self.client.get('/Listar_livros/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Excluir_livro(self):
        self.client.force_login(self.gerente)
        response = self.client.delete(f'/Excluir_livro/{self.livro.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_Liberar_emprestimo(self):
        self.client.force_login(self.funcionario)
        data = {'cpf': 'usuario', 'senha': '12345'}
        response = self.client.post('/Liberar_emprestimo/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_Renovar_emprestimo(self):
        self.client.force_login(self.funcionario)
        response = self.client.get(f'/Renovar_emprestimo/{self.emprestimo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Cancelar_emprestimo(self):
        self.client.force_login(self.funcionario)
        response = self.client.delete(f'/Cancelar_emprestimo/{self.emprestimo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_Home(self):
        self.client.force_login(self.funcionario)
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
