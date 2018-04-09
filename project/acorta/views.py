from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from urllib.parse import unquote

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
    
    return HttpResponse("Has enviado " + request.POST['URL'])

    
