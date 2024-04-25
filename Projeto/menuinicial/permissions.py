from rest_framework.permissions import BasePermission

class FuncionarioPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='funcionarios').exists()

class GerentePermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='gerente').exists()