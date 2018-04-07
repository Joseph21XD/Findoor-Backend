from django.contrib import admin
from .models import Persona, Sitio, Favorito, Visitado, Seguidor, Calificacion, Recomendacion, Comentario

admin.site.register(Persona)
admin.site.register(Sitio)
admin.site.register(Visitado)
admin.site.register(Seguidor)
admin.site.register(Calificacion)
admin.site.register(Favorito)
admin.site.register(Recomendacion)
admin.site.register(Comentario)

# Register your models here.
