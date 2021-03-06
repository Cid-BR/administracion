
import json

from django.contrib.postgres.search import SearchVector
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.caja.models import Caja
from apps.common import validaciones
from apps.inventario.models import Articulos, Inventario
from apps.servicios.models import Servicio, TipoServicio
from apps.ventas.models import Venta
from apps.cloud.views import send_to_api

from .forms import FacturaArticuloForm, FacturaForm, ServicioRapidoForm
from .models import Factura, FacturaArticulos, FacturaServicios


@login_required(login_url='login')  # redirect when user is not logged in
def facturas(request):
    """Ver todas las facturas"""
    lista_facturas = Factura.objects.filter(abierto=False)
    lista_pendientes = Factura.objects.filter(abierto=False, pago='credito')
    abiertas = Factura.objects.filter(abierto=True).count
    lista_abiertas = Factura.objects.filter(abierto=True)
    total_sin_pagar = total_facturas(lista_pendientes)
    return render(request, 'facturas/facturas.html', {
        'facturas': lista_facturas,
        'abiertas': abiertas,
        'lista_abiertas': lista_abiertas,
        'lista_pendientes': lista_pendientes,
        'total_sin_pagar': total_sin_pagar,
        'form_factura': FacturaForm,
    })


def total_facturas(facturas):
    total = 0
    for factura in facturas:
        total += factura.total
    return total


def facturas_pagadas(request):
    """Muestra las facturas que ya fueron pagadas"""
    lista_facturas = Factura.objects.filter(cerrada=True)
    pendientes = Factura.objects.filter(cerrada=False).count
    return render(request, 'facturas/facturas.html', {
        'facturas': lista_facturas,
        'pendientes': pendientes,
    })


def facturas_pendientes(request):
    """Muestra las facturas que ya fueron pagadas"""
    lista_facturas = Factura.objects.filter(cerrada=False)
    pendientes = Factura.objects.filter(cerrada=False).count
    return render(request, 'facturas/facturas.html', {
        'facturas': lista_facturas,
        'pendientes': pendientes,
    })


def nueva_factura(request):
    """Crear un nuevo factura"""
    response_data = {}
    if Caja.objects.count() > 0:
        if request.method == "POST":
            form = FacturaForm(request.POST)
            if form.is_valid():
                print('form is valid :D')
                factura = form.save(commit=False)
                factura.usuario = request.user
                factura.save()

                response_data['result'] = 'Se creó la factura.'
                response_data['id'] = str(factura.pk)
                response_data['cliente'] = str(factura.cliente)
                response_data['pago'] = str(factura.pago)

                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json")
            else:
                return HttpResponse(
                    json.dumps({'result': 'Los datos no son válidos'}),
                    content_type="application/json",
                    status=500,)

        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json",
                status=500,
            )
    else:
        response_data['result'] = 'Aún no se rea realizado la apertura de caja.'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=500,
        )


def cobrar_factura(request, pk):
    """Realiza el cobro de la Factura"""
    factura = get_object_or_404(Factura, pk=pk)
    servicios_count = FacturaArticulos.objects.filter(factura=factura).count()
    articulos_count = FacturaServicios.objects.filter(factura=factura).count()
    items_count = (servicios_count + articulos_count)

    if Caja.objects.count() > 0:
        if items_count < 1:
            messages.error(request, "No se puede cobrar una factura sin items")
            return redirect('facturas_pagadas')
        else:
            if request.method == "POST":
                # Obtener todos los items articulos y servicios de la factura
                articulos = FacturaArticulos.objects.filter(factura=factura)
                servicios = FacturaServicios.objects.filter(factura=factura)

                # Realizar la venta de cada articulo
                for articulo in articulos:
                    Venta.objects.create(
                        usuario=request.user,
                        articulo=articulo.articulo,
                        cantidad=articulo.cantidad,
                        factura=factura,
                        total=(articulo.cantidad * articulo.articulo.precio_venta))
                    inventario = Inventario.objects.get(
                        articulo=articulo.articulo)
                    inventario.existencias -= articulo.cantidad
                    inventario.save()

                # Realizar la venta de cada servicio
                for servicio in servicios:
                    Servicio.objects.create(
                        usuario=request.user,
                        descripcion=servicio.tipo_servicio.nombre,
                        cantidad=servicio.cantidad,
                        tipo_servicio=servicio.tipo_servicio,
                        factura=factura,
                        precio=(servicio.tipo_servicio.costo * servicio.cantidad))

                if factura.pago == 'contado':
                    # Guardar el monto en caja
                    caja = Caja.objects.last()
                    caja.saldo += factura.total
                    caja.save()
                    factura.estado = 'pagado'
                    factura.save()

                    # Enviar los datos a la api
                    data = {
                        'total': str(caja.saldo),
                        'date_open': str(caja.fecha_apertura),
                        'date_close': str(caja.fecha_cierre)
                    }
                    send_to_api(data, 'cashes')

                factura.abierto = False
                factura.fecha_limite = request.POST.get('fecha_limite')
                factura.save()

                # Enviar los datos a la api
                credito = None
                if factura.pago == 'credito':
                    credito = True
                else:
                    credito = False

                data = {"client": str(factura),
                        "products": articulos_count,
                        "services": servicios_count,
                        "total": str(factura.total),
                        "credit": credito,
                        "code": factura.id,
                        "seller": str(factura.usuario),
                        "date_open": str(factura.fecha_factura),
                        "date_charged": str(factura.fecha_cobro)}
                send_to_api(data, 'invoices')

                return HttpResponse(
                    json.dumps({'result': 'Se cerró la factura', 'id': str(factura.id)}),
                    content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({'result': 'No se puede cerrar la factura'}),
            content_type="application/json",
            status=500)


def eliminar_factura(request, pk):
    """Elimina una factura, solo si no ha sido cerrada"""
    if request.method == 'POST':
        factura = get_object_or_404(Factura, pk=pk)

        if validaciones.es_administrador(request.user) and factura.cerrada is False:
            factura.delete()
            messages.success(request, "Se borró la factura")

            return HttpResponse(
                json.dumps({'result': 'Se eliminó la factura'}),
                content_type="application/json")

        elif factura.usuario == request.user:
            factura.delete()
            messages.success(request, "Se borró la factura")

            return HttpResponse(
                json.dumps({'result': 'Se eliminó la factura'}),
                content_type="application/json")

        else:
            return HttpResponse(
                json.dumps({'result': 'No se puede eliminar la factura'}),
                content_type="application/json",
                status=500)



def agregar_articulo(request, pk):
    """Agrega items a la factura abierta"""
    factura = get_object_or_404(Factura, pk=pk)
    response_data = {}
    if request.method == "POST":
        form = FacturaArticuloForm(request.POST)
        if form.is_valid():
            item_articulos = form.save(commit=False)
            item_articulos.factura = factura

            inventario = get_object_or_404(
                Inventario, articulo=item_articulos.articulo)
            if item_articulos.cantidad < inventario.existencias:
                item_articulos.save()

                # Suma al total de la factura
                articulo = Articulos.objects.get(id=item_articulos.articulo.id)
                factura.total += (articulo.precio_venta *
                                  item_articulos.cantidad)
                factura.save()

                # Devolver un json con los datos del articulo
                response_data['result'] = 'Se agregó el articulo'
                response_data['item_id'] = item_articulos.pk
                response_data['articulo'] = str(item_articulos.articulo)
                response_data['articulo_id'] = str(item_articulos.articulo.id)
                response_data['precio'] = str(
                    item_articulos.articulo.precio_venta)
                response_data['cantidad'] = str(item_articulos.cantidad)
                response_data['total_factura'] = str(factura.total)
            else:
                # Devolver una excepcion por que o hay suficientes articulos
                response_data['result'] = 'No hay suficientes articulos para vender'
                response_data['reason'] = 'Existencias disponibles: ' + \
                    str(inventario.existencias)
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json",
                    status=410,
                )

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def eliminar_articulos(request, articulo):
    """Elimina un item de la factura"""
    item = get_object_or_404(FacturaArticulos, pk=articulo)
    item.delete()

    # Resta la cantidad del total
    factura = Factura.objects.get(id=item.factura.id)
    factura.total -= (item.articulo.precio_venta * item.cantidad)
    factura.save()

    messages.success(request, "Se borró el item de la factura")
    return redirect('detalles_factura', item.factura.id)


def agregar_servicio(request, pk):
    """Agrega items a la factura abierta"""
    response_data = {}
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == "POST":
        form = ServicioRapidoForm(request.POST)
        if form.is_valid():
            item_servicio = form.save(commit=False)
            item_servicio.factura = factura
            item_servicio.save()

        # Suma al total de la factura
        servicio = TipoServicio.objects.get(id=item_servicio.tipo_servicio.id)
        factura.total += (servicio.costo * item_servicio.cantidad)
        factura.save()

        # Devolver un json con los datos del articulo
        response_data['result'] = 'Se agregó el '
        response_data['item_id'] = item_servicio.pk
        response_data['servicio'] = str(item_servicio.tipo_servicio)
        response_data['servicio_id'] = str(item_servicio.tipo_servicio.id)
        response_data['costo'] = str(item_servicio.tipo_servicio.costo)
        response_data['cantidad'] = str(item_servicio.cantidad)
        response_data['total_factura'] = str(factura.total)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def eliminar_servicios(request, servicio):
    """Elimina un item de la factura"""
    item = get_object_or_404(FacturaServicios, pk=servicio)
    item.delete()

    # Resta la cantidad del total
    factura = Factura.objects.get(id=item.factura.id)
    factura.total -= (item.tipo_servicio.costo * item.cantidad)
    factura.save()

    messages.success(request, "Se borró el item de la factura")
    return redirect('detalles_factura', item.factura.id)


def detalles_factura(request, pk):
    """Muestra los detalles de una factura"""
    factura = get_object_or_404(Factura, pk=pk)
    item_articulos = FacturaArticulos.objects.filter(factura=factura).all()
    item_servicios = FacturaServicios.objects.filter(factura=factura).all()
    project_ver = settings.PROJECT_VERSION

    from apps.ajustes.models import Ajuste

    return render(request, 'facturas/detalles_factura.html', {
        'factura': factura,
        'item_articulos': item_articulos,
        'item_servicios': item_servicios,
        'form_articulo': FacturaArticuloForm,
        'form_servicio': ServicioRapidoForm,
        'project_ver': project_ver,
        'empresa': Ajuste.objects.get(pk=1) # PENDIENTE DE LIMITAR LOS CAMPOS RETORNADOS
    })


def buscar_articulo(request, codigo=None):
    '''Busca los articulos en la base de datos'''
    articulos = Articulos.objects.annotate(
        search=SearchVector('codigo', 'nombre')).filter(search=codigo)

    # Serializar el objeto que contiene los resultados la busqueda
    arts = [obj.as_dict() for obj in articulos]

    return HttpResponse(
        json.dumps(arts),
        content_type="application/json",)

    # SERVICIOS


def buscar_servicio(request, codigo):
    '''Busca servicios por su codigo o nombre'''
    tipos_servicios = TipoServicio.objects.annotate(
        search=SearchVector('codigo', 'nombre')).filter(search__icontains=codigo)

    serv = [obj.as_dict() for obj in tipos_servicios]

    return HttpResponse(
        json.dumps(serv),
        content_type="application/json")
