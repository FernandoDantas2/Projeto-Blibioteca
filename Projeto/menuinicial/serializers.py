from rest_framework import serializers
from menuinicial.models import Funcionario, Gerente, Usuario, Livro, Emprestimo

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class GerenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerente
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'

class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = '__all__'

    def validate(self, data):
        if 'data_devolucao' in data and 'data_emprestimo' in data:
         if data['data_devolucao'] < data['data_emprestimo']:
            raise serializers.ValidationError("A data de devolução deve ser posterior à data de empréstimo.")
        return data