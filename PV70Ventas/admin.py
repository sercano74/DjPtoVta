from django.contrib import admin
from PV70Ventas.models import Cliente, Producto

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display=('codigo','nombre','fono')
    search_fields=['codigo','nombre','fono']
    readonly_fields=('created','updated')
    filter_horizontal=()
    list_filter=('codigo','nombre','fono')
    fieldsets=()

admin.site.register(Cliente, ClienteAdmin)


class ProductoAdmin(admin.ModelAdmin):
    list_display=('codigo','descripcion','cantidad','costo')
    search_fields=['codigo','descripcion']
    readonly_fields=('created','updated')
    filter_horizontal=()
    list_filter=('codigo','descripcion','cantidad','costo')
    fieldsets=()

admin.site.register(Producto, ProductoAdmin)
