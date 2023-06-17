from django import forms
from PV70Ventas.models import Cliente, Producto

class AddClienteForm (forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('codigo','nombre','fono')
        labels = {
            'codigo':'Código',
            'nombre':'Nombre Completo',
            'fono':'Teléfono (Contacto)',
        }

class EditarClienteForm (forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('codigo','nombre','fono')
        labels = {
            'codigo':'Código',
            'nombre':'Nombre Completo',
            'fono':'Teléfono (Contacto)',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'type':'text', 'id':'codigo_editar'}),
            'nombre': forms.TextInput(attrs={"id":"nombre_editar"}),
            'fono':   forms.TextInput(attrs={'id':'fono_editar'}),  
            }

class AddProductoForm (forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo','descripcion','imagen','cantidad','costo')
        labels = {
            'codigo':'Código Proveedor',
            'descripcion':'Descripción',
            'imagen':'Imagen',
            'cantidad':'Cantidad (unid)',
            'costo':'Costo $',
        }

class EditarProductoForm (forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo','descripcion','imagen','cantidad','costo')
        labels = {
            'codigo':'Código Proveedor',
            'descripcion':'Descripción',
            'imagen':'Imagen',
            'cantidad':'Cantidad (unid)',
            'costo':'Costo $',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'type':'text', 'id':'codigo_editar'}),
            'descripcion': forms.TextInput(attrs={"id":"descripcion_editar"}),
            'cantidad':   forms.TextInput(attrs={'id':'cantidad_editar'}), 
            'costo':   forms.TextInput(attrs={'id':'costo_editar'}),   
            }
        
class ProductForm(forms.Form):
    codigo = forms.CharField(label="Código",max_length=200, required=True)
    #descripcion = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={'row':5}))
    descripcion = forms.CharField(label="Descripción")
    imagen = forms.ImageField()
    costo = forms.DecimalField()
    cantidad = forms.DecimalField()
    #category = forms.ModelChoiceField(label="Categoría", queryset=Category.objects.all())


