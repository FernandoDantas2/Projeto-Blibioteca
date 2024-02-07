from rest_framework import serializers
from menuinicial.models import funcionario, gerente,Usuario,Livro,Emprestimo

class funcionarioSerializer(serializers.ModelSerializer):
  class meta:
       model = funcionario
       fields = '__all__'
       extra_kwargs ={'password':{'write-olny': True}}
       
class gerenteSerializer(serializers.ModelSerializer):
    class meta:
        model = gerente
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
   class meta:
     model = Usuario
     fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
  class meta:
    model = Livro
    fields = '__all__'
    
class EmprestimoSerializer(serializers.ModelSerializer):
  class meta:
    model = Emprestimo
    fields = '__all__'
    
    def validate(self,data):
      if data['data_devolucao'] < data['data_emprestimo']:
        raise serializers.ValidationError()
      return data