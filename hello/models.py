from django.db import models

	
class Sitio(models.Model):
	nombre = models.CharField(max_length=30)
	latitud=	models.CharField(max_length=15)
	longuitud=	models.CharField(max_length=15)
	direccion = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=50)
	imagen = models.CharField(max_length=200)
	
	def __str__(self):
            return self.nombre
			
			
class Persona(models.Model):
	nombre = models.CharField(max_length=15)
	apellido = models.CharField(max_length=15)
	isFacebook = models.IntegerField()
	correo= models.CharField(max_length=30)
	contrasenna= models.CharField(max_length=20)
	imagen = models.CharField(max_length=200)
	token = models.CharField(max_length= 20)
	
	def __str__(self):
            return self.nombre
			
class Recomendacion(models.Model):
	nombre = models.CharField(max_length=30)
	latitud=	models.CharField(max_length=15)
	longuitud=	models.CharField(max_length=15)
	direccion = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=50)
	imagen = models.CharField(max_length=200)
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	
	def __str__(self):
            return self.nombre+"-"+self.persona.nombre
			
class Calificacion(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	sitio= models.ForeignKey(Sitio, on_delete=models.CASCADE)
	rate = models.IntegerField(blank=True)
	def __str__(self):
            return self.persona.nombre+"-"+self.persona.apellido+"-"+self.sitio.nombre
			
class Comentario(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	sitio= models.ForeignKey(Sitio, on_delete=models.CASCADE)
	comentario = models.CharField(max_length=200)
	def __str__(self):
            return self.persona.nombre+"-"+self.persona.apellido+"-"+self.sitio.nombre
	
class Visitado(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	sitio= models.ForeignKey(Sitio, on_delete=models.CASCADE)
	def __str__(self):
            return self.persona.nombre+"-"+self.persona.apellido+"-"+self.sitio.nombre
	
class Favorito(models.Model):
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	sitio= models.ForeignKey(Sitio, on_delete=models.CASCADE)
	def __str__(self):
            return self.persona.nombre+"-"+self.persona.apellido+"-"+self.sitio.nombre
	
class Seguidor(models.Model):
	seguidor = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name = "seguidor")
	seguido= models.ForeignKey(Persona, on_delete=models.CASCADE, related_name = "seguido")
	def __str__(self):
            return self.seguidor.nombre+"-"+self.seguidor.apellido+"-"+self.seguido.nombre+"-"+self.seguido.apellido
