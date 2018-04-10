from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from urllib.parse import unquote
from urllib.parse import urlsplit

from acorta.models import Url

# Create your views here.

FORMULARIO = """
<form action="/add"method="POST">
URL que quiere guardar:<br>
<input type="text" name="URL" value=><br>
<input type="submit" value="Enviar">
</form>
"""

def mainpage(request):
    data = Url.objects.all()
    resp = '<ul>'
    for url in data:
        resp += '<li>' + str(url.id) + '. ' + url.url
    resp += '</ul>'
    html = '<html><body><h1>Bienvenido al menu</h1>' + resp + FORMULARIO + '</body></html>'
    return HttpResponse(html)
    
def request_to_url(request):
    body = request.split('\r\n\r\n', 1)[1]
    return body.split('=')[1]

    # Añadimos comienzo a la URL si es necesario
def process_url(url):
    url = unquote(unquote(url))
    if not (url.startswith('http://') or url.startswith('https://')):
        url = "http://" + url
    return url
@csrf_exempt
def add(request):
    url=Url(url=process_url(request.POST['URL']))
    url.save()
    return HttpResponse("Has enviado " + url.url)
    
def redirect(request, code):
    

    
