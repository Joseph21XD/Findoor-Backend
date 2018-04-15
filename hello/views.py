from django.shortcuts import render
from django.http import HttpResponse
from .models import Persona, Sitio, Visitado, Favorito, Comentario, Recomendacion, Calificacion, Seguidor
from django.http import Http404
import string
import random


def lista_persona(lista, token):
		personas= "{ personas : ["
		for i in range(len(lista)):
			if(i!=len(lista)-1):
				personas+="{ id : "+parsear(str(lista[i].id))+" , nombre : "+parsear(lista[i].nombre)+" , apellido : "+parsear(lista[i].apellido)+" , imagen : "+parsear(lista[i].imagen)+" } ,"
			else:
				personas+="{ id : "+parsear(str(lista[i].id))+" , nombre : "+parsear(lista[i].nombre)+" , apellido : "+parsear(lista[i].apellido)+" , imagen : "+parsear(lista[i].imagen)+" }"
		personas+="] , token : "+token+" }"
		return personas
	
def personJson(request, tok):
	validate= Persona.objects.filter(token=tok)	
	if(len(validate)>0):
		lista=Persona.objects.all()
		validate[0].token=getToken()
		validate[0].save()
		if(len(lista)==0):
			return HttpResponse("")
		return HttpResponse(lista_persona(lista, validate[0].token))
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
		return HttpResponse(lista_persona(lista, validate[0].token))
	else:
		raise Http404
	
def person_add(request, name, lastName, isFace, mail, pwd, img):
	mail= deparsear(mail)
	validate= Persona.objects.filter(correo=mail)
	if(len(validate)==0):
		name= deparsear(name)
		lastName= deparsear(lastName)
		pwd= deparsear(pwd)
		img= deparsear(img)
		i= len(Persona.objects.all())
		tok=getToken()
		p= Persona(nombre= name, apellido= lastName,  isFacebook= isFace, correo=mail , contrasenna= pwd, imagen= img, token= tok)
		p.save()
		k= len(Persona.objects.all())
		if( k > i):
			return HttpResponse(tok)
		else :
			raise Http404
	else:
		raise Http404

def person_update(request,id_persona, name, lastName, isFace,mail, pwd, img, tok):
	validate= Persona.objects.filter(id=id_persona, token=tok)
	if(len(validate)>0):
		validate[0].nombre=deparsear(name)
		validate[0].apellido=deparsear(lastName)
		validate[0].isFacebook=isFace
		validate[0].contrasenna=deparsear(pwd)
		validate[0].correo= deparsear(mail)
		validate[0].imagen= deparsear(img)
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
	mail=deparsear(mail)
	pwd=deparsear(pwd)
	person= Persona.objects.filter(correo=mail, contrasenna= pwd)
	if(len(person)>0):
		persona="{ id : "+str(person[0].id)+" , nombre : "+parsear(person[0].nombre)+" , apellido : "+parsear(person[0].apellido)+" , imagen : "+parsear(person[0].imagen)+" , isface : "+parsear(str(person[0].isFacebook))+" , correo : "+parsear(person[0].correo)+" , contrasenna : "+parsear(person[0].contrasenna)+" , token : "+person[0].token+" }"
		return HttpResponse(persona)
	else:
		raise Http404
			
def loginByToken(request, tok):
	person= Persona.objects.filter(token=tok)
	if(len(person)>0):
		persona="{ id : "+str(person[0].id)+" , nombre : "+parsear(person[0].nombre)+" , apellido : "+parsear(person[0].apellido)+" , imagen : "+parsear(person[0].imagen)+" , isface : "+parsear(str(person[0].isFacebook))+" , correo : "+parsear(person[0].correo)+" , contrasenna : "+parsear(person[0].contrasenna)+" , token : "+person[0].token+" }"
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
				sites+="{ id : "+str(lista[i].id)+" , nombre : "+ parsear(lista[i].nombre) +" , latitud : "+parsear(lista[i].latitud)+" , longuitud : "+parsear(lista[i].longuitud)
				sites+=" , imagen : "+parsear(lista[i].imagen)+" , descripcion : "+ parsear(lista[i].descripcion) +" , direccion : "+parsear(lista[i].direccion)+" } , "
			else:
				sites+="{ id : "+str(lista[i].id)+" , nombre : "+ parsear(lista[i].nombre) +" , latitud : "+parsear(lista[i].latitud)+" , longuitud : "+parsear(lista[i].longuitud)
				sites+=" , imagen : "+parsear(lista[i].imagen)+" , descripcion : "+ parsear(lista[i].descripcion) +" , direccion : "+parsear(lista[i].direccion)+" } "
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
	comment= deparsear(comment)
	if(len(validate)>0):
		site= Sitio.objects.filter(id= id_site)
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
				comments+="{ id : "+str(lista[i].id)+" , nombre : "+parsear(lista[i].persona.nombre)+" , apellido : "+parsear(lista[i].persona.apellido)+" , imagen : "+parsear(lista[i].persona.imagen)
				comments+=", comentario : "+parsear(lista[i].comentario)+" } , "
			else:
				comments+="{ id : "+str(lista[i].id)+" , nombre : "+parsear(lista[i].persona.nombre)+" , apellido : "+parsear(lista[i].persona.apellido)+" , imagen : "+parsear(lista[i].persona.imagen)
				comments+=", comentario : "+parsear(lista[i].comentario)+" } "
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
		desc= deparsear(desc)
		dir= deparsear(dir)
		img= deparsear(img)
		lat= deparsear(lat)
		lon= deparsear(lon)
		nom= deparsear(nom)
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
		sites= sitioToJson(lista, tok)
		return HttpResponse(sites)
	else:
		raise Http404

def sitio_close(request, lat , lon, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		lat= coorToInt(deparsear(lat))
		lon= coorToInt(deparsear(lon))
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
	
def parsear(s):
    dict_1= {":":"D", "/":"S",".":"P","_":"R","-":"G",",":"C","&":"A","%":"V","=":"E","?":"I","@":"K",
         "!":"U","#":"W","¡":"B","¿":"F","<":"H",">":"J","[":"L","]":"M","(":"N",")":"O","\n":"Q",
         "\"":"T"," ":"X",";":"Y", "$":"Z"}
    lista= list(s)
    resultado=""
    for i in lista:
        if(i in dict_1):
            resultado+=dict_1[i]
        elif(i.islower() or i.isdigit()):
            resultado+=i
        elif(i.isupper()):
            resultado+="_"+i.lower()
    return resultado

def deparsear(s):
    dict_1= {"D":":", "S":"/","P":".","R":"_","G":"-","C":",","A":"&","V":"%","E":"=","I":"?","K":"@",
         "U":"!","W":"#","B":"¡","F":"¿","H":"<","J":">","L":"[","M":"]","N":"(","O":")","Q":"\n",
         "T":"\"","X":" ","Y":";", "Z":"$"}
    lista= list(s)
    resultado=""
    est= True
    for i in lista:
        if(est==False):
            resultado+=i.upper()
            est= True
        elif(i in dict_1):
            resultado+=dict_1[i]
        elif(i.islower() or i.isdigit()):
            resultado+=i
        elif(i == "_"):
            est= False
    return resultado
	
def coorToInt(coor):
	lista= list(coor)
	i= lista.index(".")
	lista.remove(".")
	l=[]
	l= lista[:i+3]
	return int("".join(l))
	
def index(request):
	return render(request, 'index.html')
	
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
				personas+="{ id : "+str(lista[i].seguidor.id)+" , nombre : "+parsear(lista[i].seguidor.nombre)+" , apellido : "+parsear(lista[i].seguidor.apellido)+" , imagen : "+parsear(lista[i].seguidor.imagen)+" } ,"
			else:
				personas+="{ id : "+str(lista[i].seguidor.id)+" , nombre : "+parsear(lista[i].seguidor.nombre)+" , apellido : "+parsear(lista[i].seguidor.apellido)+" , imagen : "+parsear(lista[i].seguidor.imagen)+" }"
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
				personas+="{ id : "+str(lista[i].seguido.id)+" , nombre : "+parsear(lista[i].seguido.nombre)+" , apellido : "+parsear(lista[i].seguido.apellido)+" , imagen : "+parsear(lista[i].seguido.imagen)+" } ,"
			else:
				personas+="{ id : "+str(lista[i].seguido.id)+" , nombre : "+parsear(lista[i].seguido.nombre)+" , apellido : "+parsear(lista[i].seguido.apellido)+" , imagen : "+parsear(lista[i].seguido.imagen)+" }"
		personas+="] , token :"+validate[0].token+" }"
		return HttpResponse(personas)
	else:
		raise Http404	

def get_seguido(request, id_persona, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		persona= Persona.objects.filter(id= id_persona) 
		lista= Seguidor.objects.filter(seguidor= validate[0], seguido= persona[0])
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		personas=""
		if(len(lista)>0):
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
		cal= Calificacion.objects.filter(persona= validate[0], sitio= site)
		if(len(cal)>0):
			cal[0].rate= rank
			cal[0].save()
		else:
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
	
def sitio_type_get(request,type,  id_site, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		k= getToken()
		validate[0].token= k
		validate[0].save()
		site= Sitio.objects.get(id= id_site)
		if(type=="VISITED"):
			visita= Visitado.objects.filter(persona=validate[0], sitio= site)
			personas=""
			if(len(visita)>0):
				personas="{ respuesta : True , token : " +validate[0].token+" }"
			else:
				personas="{ respuesta : False , token : "+validate[0].token+" }"
			return HttpResponse(personas)
		elif(type=="FAVORITE"):
			favorito= Favorito.objects.filter(persona=validate[0], sitio= site)
			personas=""
			if(len(favorito)>0):
				personas="{ respuesta : True , token : " +validate[0].token+" }"
			else:
				personas="{ respuesta : False , token : "+validate[0].token+" }"
			return HttpResponse(personas)
		raise Http404
	else:
		raise Http404
		
def sitio_type_delete(request,type,id_site,tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		k= getToken()
		validate[0].token= k
		validate[0].save()
		site= Sitio.objects.get(id= id_site)
		if(type=="VISITED"):
			visita= Visitado.objects.filter(persona=validate[0], sitio= site)
			visita[0].delete()
			return HttpResponse(k)
		elif(type=="FAVORITE"):
			favorito= Favorito.objects.filter(persona=validate[0], sitio= site)
			favorito[0].delete()
			return HttpResponse(k)
		raise Http404
	else:
		raise Http404

def seguido_delete(request, id_persona, tok):
	validate= Persona.objects.filter(token=tok)
	if(len(validate)>0):
		persona= Persona.objects.get(id= id_persona)
		seg= Seguidor.objects.filter(seguidor= validate[0], seguido= persona)
		seg[0].delete()
		tok= getToken()
		validate[0].token= tok
		validate[0].save()
		return HttpResponse(tok)
	else:
		raise Http404


	