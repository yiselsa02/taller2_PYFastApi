from django.urls import path
from . import views


urlpatterns = [

    path("", views.catalogo, name="catalogo"),

    path("checkout/", views.checkout, name="checkout"),

    path(
        "productos/nuevo/",
        views.crear_producto,
        name="crear_producto"
    ),

    path(
        "productos/<str:producto_id>/editar/",
        views.editar_producto,
        name="editar_producto"
    ),

    path(
        "productos/<str:producto_id>/eliminar/",
        views.eliminar_producto,
        name="eliminar_producto"
    ),

]