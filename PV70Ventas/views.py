from django.shortcuts import get_object_or_404, render, redirect
from .models import Cliente, Producto, Egreso, ProductosEgreso
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm, EditarProductoForm, ProductForm
from django.contrib import messages
from django.views.generic import ListView, View, UpdateView
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
# from weasyprint import HTML, CSS
# from weasyprint.text.fonts import FontConfiguration
from django.conf import settings
import os
from django.urls import reverse_lazy

# Create your views here.

def ventas_view (request):
    num_ventas = 156
    context = {
        'num_ventas':num_ventas
    }
    return render(request,'ventas.html', context)

def clientes_view (request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()
    num_clientes = clientes.count()
    context = {
        'clientes':clientes,
        'form_personal':form_personal,
        'form_editar':form_editar,
        'num_clientes':num_clientes}
    return render(request,'clientes.html', context)

class clientes2_view(View):
    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all()
        num_clientes = clientes.count()
        form_personal = AddClienteForm()
        form_editar = EditarClienteForm()
        context = {
            'clientes': clientes, 
            'num_clientes': num_clientes, 
            'form_personal':form_personal,
            'form_editar':form_editar}
        return render(request, 'clientes2.html', context)   


def add_cliente_view(request):
    if request.method == 'GET':
        form = AddClienteForm(request.POST)
    if request.POST:
        form = AddClienteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
            except:
                messages(request, 'Error al guardar!!')
                return redirect('Clientes', messages)
    return redirect('Clientes')

def edit_cliente_view(request):
    if request.method == 'POST':
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        print('Código cliente: ',cliente.codigo,'Nombre Actual del cliente: ',cliente.nombre,)
        form = EditarClienteForm(request.POST, instance = cliente)
        if form.is_valid():
            print('Nombre nuevo: ',cliente.nombre)
            form.save()
    return redirect('Clientes')

# class edit_cliente2_view(UpdateView):
#     model=Cliente
#     fields=['codigo','nombre','fono']
#     template_name='EditarPersonalModal'
#     def get_success_url(self):
#         pk=self.kwargs['pk']
#         return reverse_lazy('Clientes2')

def edit_cliente2_view(request, pk):
    print('Esta es la pk del cliente: ',pk)
    cliente= Cliente.objects.get(id = pk)
    form = EditarClienteForm(instance = cliente)
    if request.method == 'POST':
        form=EditarClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('Clientes2.html')
    context ={'form': form}
    return render(request,'Clientes2.html', context )


def delete_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        # if cliente.imagen:
        #     os.remove(cliente.imagen.path)
        cliente.delete()
    return redirect('Clientes')

def productos_view (request):
    productos = Producto.objects.all()
    form_producto = AddProductoForm()
    form_editar = EditarProductoForm()
    num_productos = productos.count()

    context = {
        'productos':productos,
        'form_producto':form_producto,
        'form_editar':form_editar,
        'num_productos':num_productos,
    }
    return render(request,'productos.html', context)

def add_producto_view(request):
    if request.POST:
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
            except:
                messages(request, 'Error al guardar!!')
                return redirect('Productos', messages)
    return redirect('Productos')

def edit_producto_view(request):
    if request.POST:
        print(request.POST['codigo'])
        producto = Producto.objects.get(pk=request.POST.get('id_producto_editar'))
        form = EditarProductoForm(request.POST, request.FILES, instance = producto)
        if form.is_valid():
            print(producto.codigo)
            form.save()
    return redirect('Productos')

class add_ventas(ListView):
    template_name = 'add_ventas.html'
    model = Egreso

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    """
    def get_queryset(self):
        return ProductosPreventivo.objects.filter(
            preventivo=self.kwargs['id']
        )
    """
    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)


def export_pdf_view(request, id, iva):
    #print(id)
    template = get_template("ticket.html")
    #print(id)
    subtotal = 0 
    iva_suma = 0 

    venta = Egreso.objects.get(pk=float(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
    for i in datos:
        subtotal = subtotal + float(i.subtotal)
        iva_suma = iva_suma + float(i.iva)

    empresa = "Mi empresa S.A. De C.V"
    context ={
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'items': datos, 
        'total': venta.total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
    }
    html_template = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; ticket.pdf"
    css_url = os.path.join(settings.BASE_DIR,'index\static\index\css/bootstrap.min.css')
    #HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])
   
    # font_config = FontConfiguration()
    # HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target=response, font_config=font_config,stylesheets=[CSS(css_url)])

    return response

# Ver https://www.youtube.com/@desarrollolibre/videos
def update(request,pk):
    producto= get_object_or_404(Producto, id=pk)

    """ #GET_OBJECT_OR_404  M A N U A L!!!!
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        #return HttpResponse(status=404)
        return HttpResponseNotFound()
    """

    form = ProductForm(initial={'codigo':producto.codigo, 'imagen':producto.imagen, 'descripcion':producto.descripcion, 'costo': producto.costo, 'cantidad':producto.cantidad})

    if request.method == 'POST':

        form = ProductForm(request.POST)

        if form.is_valid():

            producto.codigo = form.cleaned_data['codigo']
            producto.imagen = form.cleaned_data['imagen']
            producto.descripcion = form.cleaned_data['descripcion']
            producto.costo = form.cleaned_data['costo']
            producto.cantidad = form.cleaned_data['cantidad']

            producto.save()

            return redirect('Productos2')

        else:

            print("Inválido")

    return render(request,'productos2.html',{'form':form})




