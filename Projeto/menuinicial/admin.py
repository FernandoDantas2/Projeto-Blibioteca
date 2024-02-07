from django.contrib import admin
from menuinicial.models import funcionario, gerente,Usuario, Livro, Emprestimo

admin.site.register(funcionario)
admin.site.register(gerente)
admin.site.register(Usuario)
admin.site.register(Livro)
admin.site.register(Emprestimo)



# Register your models here.
