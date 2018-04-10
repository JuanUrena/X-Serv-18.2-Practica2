from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from urllib.parse import unquote
from urllib.parse import urlsplit

from acorta.models import Url

# Create your views here.

FORMULARIO = """
<form action=""method="POST">
URL que quiere guardar:<br>
<input type="text" name="URL" value=><br>
<input type="submit" value="Enviar">
</form>
"""
HOMEPAGE="""
<a href=/>Pagina Principal </a>
"""
@csrf_exempt
def mainpage(request):
    if request.method=='GET':
        data = Url.objects.all()
        resp = '<ul>'
        for url in data:
            resp += '<li><a href=' + str(url.id) + '>/'+ str(url.id)+ '</a>. ' + url.url
        resp += '</ul>'
        html = '<html><body><h1>Bienvenido al Acortador de URLs</h1>' + resp + FORMULARIO + '</body></html>'
        return HttpResponse(html)
    elif request.method=='POST':
        try:
            page=request.POST['URL']
            if page!="":
                urlre=Url(url=process_url(request.POST['URL']))
                urlre.save()
                return HttpResponse("<html><body>Has enviado: " + urlre.url +'</br> Esta en la dirección: <a href=' + str(urlre.id) + '>http://localhost:8000/'+str(urlre.id)+' </a></br>'+HOMEPAGE+'</body></html>')
            else:
                return HttpResponse('<html><body>Campo invalido </br>'+HOMEPAGE+'</body></html>')
        except IntegrityError:
            url=Url.objects.get(url=process_url(request.POST['URL']))
            return HttpResponse('<html><body>Ya estaba en la lista la Url, se encuentra en la dirección: <a href=' + str(url.id) + '>http://localhost:8000/'+str(url.id)+' </a></br>'+HOMEPAGE+'</body></html>')
    else:
        HttpResponseNotFound("<html><body><h1>No se ha encontrado el metodo para ese recurso</h1>"+HOMEPAGE+"</body></html>")
    
    
def request_to_url(request):
    body = request.split('\r\n\r\n', 1)[1]
    return body.split('=')[1]

    # Añadimos comienzo a la URL si es necesario
def process_url(url):
    url = unquote(unquote(url))
    if not (url.startswith('http://') or url.startswith('https://')):
        url = "http://" + url
    return url
    
def redirect(request, code):
    try:
        data = Url.objects.get(id=code)
        print(data)
        return HttpResponseRedirect(data)
    except Url.DoesNotExist: 
        return HttpResponseNotFound("<html><body><h1>No se ha encontrado</h1></br>"+HOMEPAGE+"</body></html>")
        
def notbe(request):
       return HttpResponseNotFound("<html><body><h1>No se ha encontrado</h1></br>"+HOMEPAGE+"</body></html>")
    

    
