from django.urls import path
from . import views
from .views import clientes2_view, edit_cliente2_view

urlpatterns = [
    path('', views.ventas_view, name='Ventas'),
    path('clientes/', views.clientes_view, name='Clientes'),
    path('clientes2/', clientes2_view.as_view(), name='Clientes2'),
    # path('clientes/', clientes_view.as_view(), name='Clientes'),
    path('add_cliente/', views.add_cliente_view, name='AddCliente'),
    path('edit_cliente/', views.edit_cliente_view, name='EditCliente'),
    path('edit_cliente2/', views.edit_cliente2_view, name='EditCliente2'),
    path('delete_cliente/', views.delete_cliente_view, name='DeleteCliente'), 
    path('productos/', views.productos_view, name='Productos'),
    path('add_producto/', views.add_producto_view, name='AddProducto'),
    path('edit_producto/', views.edit_producto_view, name='EditProducto'),
    path('update/<int:pk>', views.update, name='update'),
    path('add_venta/',views.add_ventas.as_view(), name='AddVenta'),
    path('export/', views.export_pdf_view, name="ExportPDF" ),
    path('export/<id>/<iva>', views.export_pdf_view, name="ExportPDF" ),
]