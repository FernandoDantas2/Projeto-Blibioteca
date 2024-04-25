from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.conf import settings


class FuncionarioManager(BaseUserManager):
    def create_user(self, email, nome, cpf, data_nascimento, telefone, endereco, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e a senha fornecidos.
        """
        if not email:
            raise ValueError('O email deve ser definido.')
        user = self.model(
            email=self.normalize_email(email),
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            telefone=telefone,
            endereco=endereco,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, cpf, data_nascimento, telefone, endereco, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e a senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, nome, cpf, data_nascimento, telefone, endereco, password, **extra_fields)

class Funcionario(AbstractBaseUser):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=9)
    endereco = models.CharField(max_length=10) 
    password = models.CharField(max_length=128, default=make_password('senha'))
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf', 'data_nascimento', 'telefone', 'endereco']

    objects = FuncionarioManager()

    def __str__(self):
        return f"{self.nome} foi cadastrado"

class GerenteManager(BaseUserManager):
    def create_user(self, cpf, password=None, **extra_fields):
        """
        Cria e salva um usuário com o cpf e a senha fornecidos.
        """
        if not cpf:
            raise ValueError('O CPF deve ser definido.')
        user = self.model(
            cpf=cpf,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o cpf e a senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(cpf, password, **extra_fields)

class Gerente(AbstractBaseUser):
    is_gerente = models.BooleanField(default=False)
    cpf = models.CharField(max_length=11, unique=True)
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'email']
    objects = GerenteManager()

    # Adicionando campo de solicitações pendentes
    solicitacoes_pendentes = models.ManyToManyField('SolicitacaoCadastro', blank=True)

    def __str__(self):
        return f"{self.username} foi cadastrado"
    
class SolicitacaoCadastro(models.Model):
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE)

    def __str__(self):
        return f"Solicitação de {self.funcionario.username}"   


class Usuario(models.Model):
    nome = models.CharField(max_length=25)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)
    senha = models.CharField(max_length=9)
    email = models.EmailField(default='example@example.com')
    idade = models.IntegerField(default=0)
    data_nascimento = models.DateField(default=timezone.now)
    endereco = models.CharField(max_length=255, default='Endereço Padrão')


    def __str__(self):
        return f"O {self.nome} foi criado com sucesso"

class Livro(models.Model):
    titulo = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    editora = models.CharField(max_length=50)
    ano = models.CharField(max_length=10)

    def __str__(self):
        return f"O {self.titulo} foi adicionado com sucesso"

class Emprestimo(models.Model):
    Livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Data_emprestimo = models.DateTimeField(default=timezone.now)
    Data_devolucao = models.DateTimeField(blank=True, null=True)
    Status = models.CharField(max_length=20, default='Em andamento')
    Data_cancelamento = models.DateTimeField(blank=True, null=True)
    
    def cancelar(self):
        if self.status != 'Cancelado':
            self.status = 'Cancelado'
            self.Data_cancelamento = timezone.now()
            self.save()

    def __str__(self):
        return f"O {self.Livro} foi emprestado para {self.Usuario} no dia {self.Data_emprestimo}"
    
    def save(self, *args, **kwargs):
        if not self.Data_devolucao:
            self.Data_devolucao = self.Data_emprestimo + timedelta(days=7)
        super().save(*args, **kwargs)

# Create your models here.
