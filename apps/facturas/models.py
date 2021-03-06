
from django.db import models
from django.utils import timezone
from apps.inventario.models import Articulos
from apps.servicios.models import TipoServicio

# Create your models here.


class Factura(models.Model):
    '''Factura una venta realizada a un cliente'''
    TIPOS = (
        ('contado', 'Contado'),
        ('credito', 'Credito'))
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'))

    usuario = models.ForeignKey('auth.User')
    cliente = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    abierto = models.BooleanField(default=True)
    pago = models.CharField(max_length=15, choices=TIPOS, default='contado')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    fecha_limite = models.DateTimeField(blank=True, null=True)
    fecha_factura = models.DateTimeField(default=timezone.now)
    fecha_cobro = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.cliente

    def productos_count(self):
        '''Devolver la cantidad de productos adquiridos'''
        item_articulos = FacturaArticulos.objects.filter(factura=self).count()
        return item_articulos

    def servicios_count(self):
        '''Devuelve la cantidad de serivicios adquiridos'''
        item_servicios = FacturaServicios.objects.filter(factura=self).count()
        return item_servicios

    def clase(self):
        if self.estado == 'pagado':
            return 'success'
        elif self.pago == 'credito' and timezone.now() < self.fecha_limite:
            return 'warning'
        elif self.pago == 'credito' and timezone.now() > self.fecha_limite:
            return 'danger'
        else:
            return 'faded'
    def _vencimiento(self):
        return self.fecha_limite


class Abono(models.Model):
    '''Almacena los los abonos realizados a una factura pendiente'''
    factura = models.ForeignKey('facturas.Abono', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_abono = models.DateField(default=timezone.now)


class FacturaItems(models.Model):
    '''Almacena individualmente los items de una Factura'''
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)


class FacturaArticulos(models.Model):
    '''Almacena el articulo que se planea vender'''
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)


class FacturaServicios(models.Model):
    '''Almacena el articulo que se planea vender'''
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
