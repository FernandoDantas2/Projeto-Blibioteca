from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import authenticate,login,logout
from .serializer import funcionarioSerializer, gerenteSerializer,UsuarioSerializer,LivroSerializer,EmprestimoSerializer
from menuinicial.models import funcionario,gerente,Usuario,Livro,Emprestimo
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login_gerente(request):
   if request.method == 'POST':
    Username = request.data.get('nome')
    Password = request.data.get('senha')
    user = authenticate(request, Username=Username, Password=Password)
    if User is not None and User.is_staff:
       login(request = User)
       return Response(status=status.HTTP_200_OK)
    else:
       return Response(status=status.HTTP_401_UNAUTHORIZED)
 
@api_view(['POST'])
def logout_gerente(request):
    if request.method == 'POST':
     logout(request)  
     return Response(status=status.HTTP_200_OK)
 
 
@api_view(['POST'])
def cadastrofuncionario(request):
   if request.method == 'POST':
     seralizer = funcionarioSerializer(data=request.data)
     seralizer.save()
     return Response(seralizer.data,status=status.HTTP_201_CREATED)
   else:
      return Response(seralizer.errors, status=status.HTTP_401_UNAUTHORIZED)
   
@api_view(['POST'])
def loginfuncionario(request):
   if request.method == 'POST':
      Username = request.data.get('nome')
      Password = request.data.gete('senha')
      User = authenticate(request, Username=Username , Password=Password)
      if User is not None and User.is_staff:
         funcionario (request = User)
         return Response(status=status.HTTP_200_OK)
      else:
         return Response(status=status.HTTP_401_UNAUTHORIZED) 
      

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excluir_funcionario(request, id):
   try:
     funcionario = funcionario.objetcs.get(pk=id)
   except funcionario.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
   
   #verificando ja que só o gerente pode excluir o funcionario
   if not request.user.is_gerente:    
      return Response({'message': 'Apenas gerentes podem excutar essa ação'})
   if request.method == 'DELETE':
      funcionario.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
   

api_view(['POST'])
@permission_classes([IsAuthenticated])
def cadastra_livro(request):
   if request.method == 'POST':
    Serializer = LivroSerializer(data=request.data)
    if Serializer.is_valid():
     Serializer.save()
     return Response(Serializer.data, status=status.HTTP_201_CREATED)
    return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                  
class gerenteViewset(viewsets.ModelViewSet):
   queryset = gerente.objects.all()
   serializer_class = gerenteSerializer 
   permission_classes = [permissions.IsAuthenticated]

class funcionarioViewset(viewsets.ModelViewSet):
   queryset = funcionario.objects.all()
   serializer_clas = funcionarioSerializer
   permission_classes = [permissions.IsAuthenticated]
   

class UsuarioViewset(viewsets.ModelViewSet):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer 
     
   def create(self, request):
      data = request.data
    
      grupo = Group.objects.get(name = 'usuario')
      Usuario = User.objects.create_user(
         
         username = data['username'],
         password = data['senha'],      
      )
      Usuario.groups.add(grupo)
    
      Usuario = Usuario.objects.create(
          nome=data ['nome'],
          cpf = data ['cpf'],  
          senha=data['senha'],
          telefone=data['telefone'],
      )
      Usuario.save()
      serializerUsuario = UsuarioSerializer(Usuario)
      return Response(
          {"saida":'Usuario criado com sucesso!',"data":serializerUsuario.data},
          status= status.HTTP_201_CREATED   
      )

class LivroViewset(viewsets.ModelViewSet):
   queryset = Livro.objects.all()
   serializer_class = LivroSerializer
   permission_classes = [permissions.IsAuthenticated]
  
class EmprestimoViewset(viewsets.ModelViewSet):
   queryset = Emprestimo.objects.all()
   serializer_class = EmprestimoSerializer














   
   
   
   # poderia utilziar outro metodo de permissão permission_classes = [permissions.IsAuthenticated]
   
   
   
   
   
   
   
   
   
   

   
   
   
   
   
   
   
   
   
   
   