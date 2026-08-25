import requests
from django.shortcuts import render


def catalogo(request):

    url = "http://127.0.0.1:8000/productos/"

    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        productos = respuesta.json()
    else:
        productos = []

    return render(
        request,
        "catalogo/catalogo.html",
        {
            "productos": productos
        }
    )