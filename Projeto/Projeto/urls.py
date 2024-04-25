from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menuinicial/', include('menuinicial.urls')),
    # Outras URLs do seu projeto aqui
]

