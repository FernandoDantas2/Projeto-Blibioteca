from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager


class funcionario(AbstractBaseUser):
   nome = models.CharField (max_length=100)
   cpf = models. CharField (max_length=11)
   data_nascimento = models.DateField()
   telefone = models.CharField(max_length=9)
   endereco = models.CharField(max_length=10) 
   passoword = models.CharField(max_length=10)
   email = models. CharField(max_length=20)
   
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['nome', 'cpf', 'data_nascimento', 'telefone', 'endereco', 'senha',]   
   
   objects = BaseUserManager()

   def __str__(self):
     return f"{self.nome} foi cadastrado"
       
   
class gerente(models.Model):
   nome = models.CharField(max_length=100)
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   senha = models.CharField(max_length=10)
   cpf = models.CharField(max_length=11)
   
   def __str__(self):
     return f"O {self.user} foi cadastrado "
   

class Usuario(models.Model):
  nome = models.CharField(max_length=50)
  cpf = models.CharField(max_length=11)
  senha = models.CharField(max_length=10)
  telefone = models.CharField(max_length=11)
  
  def __str__(self):
     return f"O {self.nome} foi criado com sucesso"
  

class Livro(models.Model):
 titulo = models.CharField(max_length=50)
 autor = models.CharField(max_length=50)
 editora = models.CharField(max_length=50)
 ano = models.CharField(max_length=10)
 
 def __str__(self):
    return f"O {self.titulo} foi adicionado com sucesso "
 
class Emprestimo(models.Model):
    Livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Data_emprestimo = models.DateTimeField(default= timezone.now)
    Data_devolucao = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f" O {self.Livro} foi emprestado para {self.Usuario} no dia {self.Data_emprestimo}"
     
    
 
   

# Create your models here.
