import requests
from django.shortcuts import render, redirect


API_URL = "https://taller2-pyfastapi.onrender.com"


def catalogo(request):

    url = f"{API_URL}/productos/"

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


def checkout(request):

    if request.method == "POST":

        producto_id = request.POST.get("producto_id")
        cantidad = request.POST.get("cantidad")
        cliente = request.POST.get("cliente")

        datos = {
            "producto_id": producto_id,
            "cantidad": int(cantidad),
            "cliente": cliente
        }

        url = f"{API_URL}/pedidos/"

        respuesta = requests.post(
            url,
            json=datos
        )

        if respuesta.status_code == 200:
            return render(
                request,
                "catalogo/checkout.html",
                {
                    "mensaje": "Pedido registrado correctamente"
                }
            )

        return render(
            request,
            "catalogo/checkout.html",
            {
                "mensaje": "No se pudo registrar el pedido"
            }
        )

    return render(
        request,
        "catalogo/checkout.html"
    )


# CREATE - Crear producto
def crear_producto(request):

    if request.method == "POST":

        datos = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": float(request.POST.get("precio")),
            "stock": int(request.POST.get("stock")),
            "categoria": request.POST.get("categoria"),
            "imagen": request.POST.get("imagen")
        }

        respuesta = requests.post(
            f"{API_URL}/productos/",
            json=datos
        )

        if respuesta.status_code == 200:
            return redirect("catalogo")

    return render(
        request,
        "catalogo/producto_form.html"
    )


# UPDATE - Editar producto
def editar_producto(request, producto_id):

    if request.method == "POST":

        datos = {
            "nombre": request.POST.get("nombre"),
            "descripcion": request.POST.get("descripcion"),
            "precio": float(request.POST.get("precio")),
            "stock": int(request.POST.get("stock")),
            "categoria": request.POST.get("categoria"),
            "imagen": request.POST.get("imagen")
        }

        respuesta = requests.put(
            f"{API_URL}/productos/{producto_id}",
            json=datos
        )

        if respuesta.status_code == 200:
            return redirect("catalogo")

    respuesta = requests.get(
        f"{API_URL}/productos/{producto_id}"
    )

    producto = respuesta.json()

    return render(
        request,
        "catalogo/producto_form.html",
        {
            "producto": producto
        }
    )


# DELETE - Eliminar producto
def eliminar_producto(request, producto_id):

    if request.method == "POST":

        requests.delete(
            f"{API_URL}/productos/{producto_id}"
        )

    return redirect("catalogo")