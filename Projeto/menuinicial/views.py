from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import FuncionarioSerializer, UsuarioSerializer, LivroSerializer, EmprestimoSerializer
from menuinicial.models import Funcionario, Usuario, Livro, Emprestimo, SolicitacaoCadastro
from rest_framework.permissions import IsAuthenticated
from .permissions import FuncionarioPermissions, GerentePermissions
from datetime import datetime, timedelta

@api_view(['POST'])
def Login_gerente(request):
    if request.method == 'POST':
        username = request.data.get('nome')
        password = request.data.get('senha')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_gerente:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST'])
def Logout_gerente(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)
    return Response({'message': 'Método não permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Listar_solicitacoes(request):
    if request.user.is_gerente:
        solicitacoes = list(SolicitacaoCadastro.objects.all().values())
        return JsonResponse({'solicitacoes': solicitacoes})
    else:
        return JsonResponse({'error': 'Acesso negado'})

@api_view(['POST'])
@permission_classes([GerentePermissions])
def Cadastro_funcionario(request):
    if request.method == 'POST':
        serializer = FuncionarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "método não permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
@api_view(['POST'])
@permission_classes([GerentePermissions])
def Aprovar_solicitacao(request, solicitacao_id):
    if request.method == 'POST':
        try:
            solicitacao = SolicitacaoCadastro.objects.get(pk=solicitacao_id)
        except SolicitacaoCadastro.DoesNotExist:
            return Response({"mensagem": "Solicitação não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        solicitacao.aprovado = True
        solicitacao.save()
        return JsonResponse({'message': 'Solicitação aprovada com sucesso'})
    else:
        return Response({"error": "método não permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def Login_funcionario(request):
    if request.method == 'POST':
         username = request.data.get('username')
         password = request.data.get('password')
         user = authenticate(request, username=username, password=password)
         if user is not None:
             login(request, user)
             return JsonResponse({'message': 'Login successful'}, status=200)
         else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['POST'])
def Logout_funcionario(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)
    return Response({'message': 'Método não permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
@permission_classes([GerentePermissions])
def Excluir_funcionario(request, id):
    try:
        funcionario = Funcionario.objects.get(pk=id)
    except Funcionario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    funcionario.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Cadastra_usuario(request):
    if request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Cadastra_livro(request):
    if request.method == 'POST':
        serializer = LivroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated, FuncionarioPermissions])
def Listar_livros(request):
    if request.method == 'POST':
        serializer = LivroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        livro_id = request.data.get('id')
        try:
            livro = Livro.objects.get(pk=livro_id)
            livro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Livro.DoesNotExist:
            return Response({"mensagem": "Livro não encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, FuncionarioPermissions])
def Excluir_livro(request, livro_id):
    try:
        livro = Livro.objects.get(pk=livro_id)
    except Livro.DoesNotExist:
        return Response({"mensagem": "Livro não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    livro.delete()
    return Response({"mensagem": "Livro excluído com sucesso"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def Liberar_emprestimo(request):
    if request.method == 'POST':
        data_devolucao = datetime.now() + timedelta(days=7)
        request.data['data_devolucao'] = data_devolucao.strftime("%Y-%m-%d")
       
        cpf = request.data.get('cpf')
        senha = request.data.get('senha')
        try:
            user = User.objects.get(username=cpf)
            if not user.check_password(senha):
                return Response({'message': 'Senha inválida.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'message': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        request.data['usuario'] = user.id
        serializer = EmprestimoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Renovar_emprestimo(request, emprestimo_id):
    try:
        emprestimo = Emprestimo.objects.get(pk=emprestimo_id)
        emprestimo.renovar()
        serializer = EmprestimoSerializer(emprestimo)
        return Response(serializer.data)
    except Emprestimo.DoesNotExist:
        return Response({"mensagem": "emprestimo não encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Cancelar_emprestimo(request, emprestimo_id):
    try:
        emprestimo = Emprestimo.objects.get(pk=emprestimo_id)
        emprestimo.cancelar()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Emprestimo.DoesNotExist:
        return Response({"message": "Empréstimo não encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Home(request):
    if request.user.is_authenticated:
        if request.user.is_funcionario:
            menus = [
                {'name': 'Cadastrar Usuário', 'url': '/cadastrar_usuario/'},
                {'name': 'Cadastrar Livros', 'url': '/cadastrar_livros/'},
                {'name': 'Buscar Livros', 'url': '/buscar_livros/'},
                {'name': 'Emprestimos', 'url': '/emprestimos/'},
                {'name': 'Remover Livros', 'url': '/remover_livros/'},
                {'name': 'Remover Usuário', 'url': '/remover_usuario/'},
                {'name': 'Logout', 'url': '/logout/'},
            ]
            return JsonResponse({'menus': menus})
    return JsonResponse({})

   # poderia utilziar outro metodo de permissão permission_classes = [permissions.IsAuthenticated]
   
   
   
   
   
   
   
   
   

   
   
   
   
   
   
   
   
   
   
   