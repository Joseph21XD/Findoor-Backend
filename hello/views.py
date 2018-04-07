from django.shortcuts import render
from django.http import HttpResponse
from .models import Persona, Sitio, Visitado, Favorito, Comentario, Recomendacion, Calificacion
from django.http import Http404
import string
import random


def personJson(request, tok):
	validate= Persona.objects.filter(token=tok)	
	if(len(validate)>0):
		lista=Persona.objects.all()
		validate[0].token=getToken()
		validate[0].save()
		if(len(lista)==0):
			return HttpResponse("")
		personas= "{ personas : ["
		for i in range(len(lista)):
			if(i!=len(lista)-1):
				personas+="{id : "+str(lista[i].id)+" , nombre : "+lista[i].nombre+" , apellido : "+lista[i].apellido+" , imagen : "+lista[i].imagen+" ,"
			else:
				personas+="{id : "+str(lista[i].id)+" , nombre : "+lista[i].nombre+" , apellido : "+lista[i].apellido+" , imagen : "+lista[i].imagen+" }"
		personas+="], token :"+validate[0].token+" }"
		return HttpResponse(personas)
	else:
		raise Http404

def person_id_Json(request, id_personaje, tok):
	validate= Persona.objects.filter(token=tok)	
	if(len(validate)>0):
		lista=Persona.objects.filter(id=id_personaje)
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		if(len(lista)==0):
			return HttpResponse("")
		persona= ""
		for i in range(len(lista)):
			if(i!=len(lista)-1):
				persona+="{ id : "+str(lista[i].id)+" , nombre  : "+lista[i].nombre+" , apellido : "+lista[i].apellido+" , imagen : "+lista[i].imagen+" , token : "+tok+" },"
			else:
				persona+="{ id : "+str(lista[i].id)+" , nombre : "+lista[i].nombre+" , apellido : "+lista[i].apellido+" , imagen : "+lista[i].imagen+" , token : "+tok+" }"
		return HttpResponse(persona)
	else:
		raise Http404
	
def person_add(request, name, lastName, isFace, mail, pwd, img):
	i= len(Persona.objects.all())
	tok=getToken()
	mail= parseURL(mail)
	p= Persona(nombre= name, apellido= lastName,  isFacebook= isFace, correo=mail , contrasenna= pwd, imagen= parseURL(img), token= tok)
	p.save()
	k= len(Persona.objects.all())
	if( k > i):
		return HttpResponse(tok)
	else :
		raise Http404

def person_update(request,id_persona, name, lastName, isFace,mail, pwd, img, tok):
	validate= Persona.objects.filter(id=id_persona, token=tok)
	if(len(validate)>0):
		validate[0].nombre=name
		validate[0].apellido=lastName
		validate[0].isFacebook=isFace
		validate[0].contrasenna=pwd
		validate[0].correo= parseURL(mail)
		validate[0].imagen= parseURL(img)
		k= getToken()
		validate[0].token=k
		validate[0].save()
		return HttpResponse(k)
	else :
		raise Http404
		
def getToken():
	lst = [random.choice(string.ascii_letters + string.digits) for n in range(20)]
	str1 = "".join(lst)
	return str1
	
def loginByCredentials(request, mail, pwd):
		mail=parseURL(mail)
		person= Persona.objects.filter(correo=mail, contrasenna= pwd)
		if(len(person)>0):
			persona="{ id : "+str(person[0].id)+" , nombre : "+person[0].nombre+" , apellido : "+person[0].apellido+" , imagen : "+person[0].imagen+" , correo : "+person[0].correo+" , contrasenna : "+person[0].contrasenna+" , token : "+person[0].token+"},"
			return HttpResponse(persona)
		else:
			raise Http404
			
def loginByToken(request, tok):
	person= Persona.objects.filter(token=tok)
	if(len(person)>0):
		persona="{ id : "+str(person[0].id)+" , nombre : "+person[0].nombre+" , apellido : "+person[0].apellido+" , imagen : "+person[0].imagen+" , correo : "+person[0].correo+" , contrasenna : "+person[0].contrasenna+" , token : "+person[0].token+"},"
		return HttpResponse(persona)
	else:
		raise Http404
			
def sitioJson(request, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		k= getToken()
		validate[0].token= k
		validate[0].save()
		sitios= Sitio.objects.all()
		sites= sitioToJson(sitios, validate[0].token)
		return HttpResponse(sites)
	else:
		raise Http404
		
def sitioToJson(lista, token):
	sites="{ sitios : ["
	for i in range(len(lista)):
			if(i!=len(lista)-1):
				sites+="{ id : "+str(lista[i].id)+" , nombre : "+ deparse(lista[i].nombre) +" , latitud : "+lista[i].latitud+" , longuitud : "+lista[i].longuitud
				sites+=" , imagen : "+lista[i].imagen+" , descripcion :"+ deparse(lista[i].descripcion) +" , direccion : "+deparse(lista[i].direccion)+" } , "
			else:
				sites+="{id : "+str(lista[i].id)+" , nombre : "+ deparse(lista[i].nombre)+" , latitud : "+lista[i].latitud+" , longuitud : "+lista[i].longuitud
				sites+=" , imagen : "+lista[i].imagen+" , descripcion : "+ deparse(lista[i].descripcion) +" , direccion : "+ deparse(lista[i].direccion)+" }"
	sites+="], token : "+token+" }"
	return sites
	
def sitio_type_Json(request, type , id_persona, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		k= getToken()
		validate[0].token= k
		validate[0].save()
		persona= Persona.objects.get(id= id_persona)
		if(type=="VISITED"):
			return HttpResponse(getVisited(persona, validate[0]))
		elif(type=="FAVORITE"):
			return HttpResponse(getFavorite(persona, validate[0]))
		raise Http404
	else:
		raise Http404

def getFavorite(id_persona,person):
	favoritos= Favorito.objects.filter(persona= id_persona)
	sitios=[]
	for i in favoritos:
		sitios.append(i.sitio)
	sites= sitioToJson(sitios, person.token)
	return sites
	
def getVisited(id_persona, person):
	visitados= Visitado.objects.filter(persona= id_persona)
	sitios=[]
	for i in visitados:
		sitios.append(i.sitio)
	sites= sitioToJson(sitios, person.token)
	return sites

def sitio_comment(request, id_site, comment, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		site= Sitio.objects.filter(id= id_site)
		comment= parseDesc(comment)
		comm= Comentario(persona= validate[0], sitio=site[0], comentario= comment)
		comm.save()
		k= getToken()
		validate[0].token= k
		validate[0].save()
		return HttpResponse(k)
	else:
		raise Http404
		
def sitio_comment_Json(request,id_site,tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		token= getToken()
		site= Sitio.objects.filter(id= id_site)
		lista= Comentario.objects.filter(sitio=site[0])
		comments="{ comentarios : ["
		for i in range(len(lista)):
			if(i!=len(lista)-1):
				comments+="{ id : "+str(lista[i].id)+" , nombre : "+lista[i].persona.nombre+" , apellido : "+lista[i].persona.apellido+" , imagen : "+lista[i].persona.imagen
				comments+=", comentario : "+lista[i].comentario+" } , "
			else:
				comments+="{ id : "+str(lista[i].id)+" , nombre : "+lista[i].persona.nombre+" , apellido : "+lista[i].persona.apellido+" , imagen : "+lista[i].persona.imagen
				comments+=", comentario : "+lista[i].comentario+" } "
		comments+="] , token : "+token+" }"
		validate[0].token= token
		validate[0].save()
		return HttpResponse(comments)
	else:
		raise Http404
		
def sitio_suggest(request,nom,lat,lon,dir,desc,img,tok):
	validate= Persona.objects.filter(token= tok)
	if(len(validate)>0):
		k= getToken()
		desc= parseDesc(desc)
		dir= parseDesc(dir)
		img= parseURL(img)
		lat= parseCoor(lat)
		lon= parseCoor(lon)
		nom= parseDesc(nom)
		suggest= Recomendacion(nombre= nom, latitud=lat, longuitud=lon,direccion=dir,descripcion=desc,imagen=img, persona=validate[0])
		suggest.save()
		validate[0].token= k
		validate[0].save()
		return HttpResponse(k)
	else:
		raise Http404

def getRanking():
	sitios= Sitio.objects.all()
	ranking= []
	sites= []
	calificaciones= Calificacion.objects.all()
	if(len(calificaciones)!=0):
		for i in calificaciones:
			if(i.sitio.id in sites):
				for j in ranking:
					if j[0]==i.sitio.id:
						j[2]+=1
						j[1]+=i.rate
						j[3]= j[1]/j[2]
			else:
				sites.append(i.sitio.id)
				ranking.append([i.sitio.id, i.rate, 1, i.rate])
		for passnum in range(len(ranking)-1,0,-1):
			for j in range(passnum):
				if ranking[j][3]<ranking[j+1][3]:
					temp= ranking[j]
					ranking[j]= ranking[j+1]
					ranking[j+1]= temp
		resultado=[]
		for k in ranking:
			a= Sitio.objects.get(id= k[0])
			resultado.append(a)
		return resultado
	else:
		return sitios

def sitio_ranking_Json(request, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		lista=[]
		lista= getRanking()
		sites="{ sitios : ["
		for i in range(len(lista)):
			if(i!=len(lista)-1):
				sites+="{ id : "+str(lista[i].id)+" , nombre : "+lista[i].nombre+" , latitud : "+lista[i].latitud+" , longuitud : "+lista[i].longuitud
				sites+=", imagen "+lista[i].imagen+", descripcion"+lista[i].descripcion+", descripcion"+lista[i].descripcion+" } , "
			else:
				sites+="{id : "+str(lista[i].id)+" , nombre : "+lista[i].nombre+" , latitud : "+lista[i].latitud+" , longuitud : "+lista[i].longuitud
				sites+=", imagen : "+lista[i].imagen+", descripcion : "+lista[i].descripcion+", direccion : "+lista[i].direccion+" }"
		sites+="], token : "+tok+" }"
		return HttpResponse(sites)
	else:
		raise Http404

def sitio_close(request, lat , lon, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		lat= coorToInt(parseCoor(lat))
		lon= coorToInt(parseCoor(lon))
		sitios= Sitio.objects.all()
		coors=[]
		for i in sitios:
			coors.append([i,coorToInt(i.latitud),coorToInt(i.longuitud)])
		lista=[]		
		for j in coors:
			if abs(lat-j[1])<=1 and abs(lon-j[2])<=1:
				lista.append(j[0])
		tok= getToken()
		validate[0].token=tok
		validate[0].save()
		return HttpResponse(sitioToJson(lista, tok))
	else:
		raise Http404
		
def parseCoor(coor):
	lista= list(coor)
	if lista[0]=="N":
		lista[0]="-"
	a= lista.index("P")
	lista[a]="."
	return "".join(lista)
	
def parseDesc(desc):
	lista= list(desc)
	while "_" in lista:
		a= lista.index("_")
		lista[a]=" "
	return "".join(lista)
	
def deparse(desc):
	lista= list(desc)
	while " " in lista:
		a= lista.index(" ")
		lista[a]="_"
	return "".join(lista)
	
def parseURL(url):
	resultado=""
	lista= list(url)
	est= False
	for i in lista:
		if est==True:
			resultado+=i.upper()
			est=False
		elif i=="D":
			resultado+=":"
		elif i=="S":
			resultado+="/"
		elif i=="P":
			resultado+="."
		elif i=="R":
			resultado+="_"
		elif i=="G":
			resultado+="-"
		elif i=="C":
			resultado+=","
		elif i=="A":
			resultado+="&"
		elif i=="V":
			resultado+="%"
		elif i=="E":
			resultado+="="
		elif i=="I":
			resultado+="?"
		elif i=="K":
			resultado+="@"
		elif i=="U":
			resultado+="!"
		elif i=="W":
			resultado+="#"
		elif i=="_":
			est=True
		else:
			resultado+=i
	return resultado
	
def coorToInt(coor):
	lista= list(coor)
	lista.remove(".")
	l=[]
	if "-" in lista:
		l= lista[:5]
	else:
		l= lista[:4]
	return int("".join(l))
	
def index(request):
	return HttpResponse("Bienvenido a Findoor!")
	
def seguir(request, id_persona, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		persona= Persona.objects.get(id= id_persona)
		seg= Seguidor(seguidor= validate[0], seguido= persona)
		seg.save()
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		return HttpResponse(tok)
	else:
		raise Http404

def seguidores(request, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		lista= Seguidor.objects.filter(seguido= validate[0])
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		personas= "{ personas : ["
		for i in range(len(lista)):
			if(i!=len(lista)-1):
				personas+="{ id : "+str(lista[i].seguidor.id)+" , nombre : "+lista[i].seguidor.nombre+" , apellido : "+lista[i].seguidor.apellido+" , imagen : "+lista[i].seguidor.imagen+" },"
			else:
				personas+="{ id : "+str(lista[i].seguidor.id)+" , nombre : "+lista[i].seguidor.nombre+" , apellido : "+lista[i].seguidor.apellido+" , imagen : "+lista[i].seguidor.imagen+" }"
		personas+="] , token :"+validate[0].token+" }"
		return HttpResponse(personas)
	else:
		raise Http404	

def seguidos(request, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		lista= Seguidor.objects.filter(seguidor= validate[0])
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		personas= "{ personas : ["
		for i in range(len(lista)):
			if(i!=len(lista)-1):
				personas+="{ id : "+str(lista[i].seguido.id)+" , nombre : "+lista[i].seguido.nombre+" , apellido : "+lista[i].seguido.apellido+" , imagen : "+lista[i].seguido.imagen+" },"
			else:
				personas+="{ id : "+str(lista[i].seguido.id)+" , nombre : "+lista[i].seguido.nombre+" , apellido : "+lista[i].seguido.apellido+" , imagen : "+lista[i].seguido.imagen+" }"
		personas+="] , token :"+validate[0].token+" }"
		return HttpResponse(personas)
	else:
		raise Http404	

def get_seguido(request, id_persona, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		persona= Persona.objects.filter(id= id_persona) 
		lista= Seguidor.objects.filter(seguidor= validate[0], seguido= persona)
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		personas=""
		if(len(persona)>0):
			personas+="{ respuesta : True , token : "+validate[0].token+" }"
		else:
			personas+="{ respuesta : False , token : "+validate[0].token+" }"
		return HttpResponse(personas)
	else:
		raise Http404	

def sitio_type_add(request, type, id_site, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		k= getToken()
		validate[0].token= k
		validate[0].save()
		site= Sitio.objects.get(id= id_site)
		if(type=="VISITED"):
			visita= Visitado(persona= validate[0], sitio= site)
			visita.save()
			return HttpResponse(k)
		elif(type=="FAVORITE"):
			favorito= Favorito(persona= validate[0], sitio= site)
			favorito.save()
			return HttpResponse(k)
		raise Http404
	else:
		raise Http404
	
def sitio_ranking_add(request, id_site, rank, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		site= Sitio.objects.get(id=id_site)
		validate[0].token= tok
		validate[0].save()
		ranked= Calificacion(persona= validate[0], sitio= site, rate=rank)
		ranked.save()
		return HttpResponse(tok)
	else:
		raise Http404

def sitio_ranking_get(request, id_site, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		site= Sitio.objects.get(id= id_site)
		calificacion= Calificacion.objects.filter(sitio= site, persona= validate[0]) 
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		personas=""
		if(len(calificacion)>0):
			personas+="{ respuesta : "+str(calificacion[0].rate)+" , token : "+validate[0].token+" }"
		else:
			personas+="{ respuesta : 0 , token : "+validate[0].token+" }"
		return HttpResponse(personas)
	else:
		raise Http404
	
