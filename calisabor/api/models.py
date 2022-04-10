from django.db import models
# from django import forms
# from djongo.models.fields import ArrayField
from django.utils.timezone import now

from django.contrib.auth import get_user_model

User = get_user_model()


class People(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name = models.CharField(max_length=200, verbose_name="Apellidos")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Profile(models.Model):
    """
    Usuarios de la app.

    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, max_length=50, on_delete=models.CASCADE, verbose_name="Cuenta de usuario")
    first_name = models.CharField(max_length=50, verbose_name="Nombres", null=True)
    last_name = models.CharField(max_length=50, verbose_name="Apellidos")
    email = models.CharField(max_length=50, verbose_name="Correo electronico")
    phone = models.CharField(max_length=32, verbose_name="Numero Telefonico")
    mobile = models.CharField(max_length=32, verbose_name="Numero Telefonico alternativo")
    profile_pic = models.CharField(max_length=250, verbose_name="Imagen de perfil", null=True)
    position = models.CharField(max_length=150, verbose_name="Rol o cargo en la empresa")
    birthday = models.DateField(blank=True, verbose_name="Fecha de cumpleaños")
    country = models.CharField(max_length=32, verbose_name="País de origen")
    city = models.CharField(max_length=32, verbose_name="Ciudad de residencia")
    login_count = models.PositiveIntegerField(default=0, verbose_name="Contador de inicios de sesión exitosos")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        db_table = 'cs_users'


class Client(models.Model):
    """

    """
    client_name = models.CharField(max_length=100, verbose_name="Nombre de empresa")
    nit = models.CharField(max_length=15, verbose_name="NIT del cliente")
    ceo_name = models.CharField(max_length=100, verbose_name="Gerente")
    ceo_phone = models.CharField(max_length=10)
    ceo_mobile = models.CharField(max_length=10)
    cco_name = models.CharField(max_length=100, verbose_name="Jefe de compras")
    cco_phone = models.CharField(max_length=10)
    cco_mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=50, verbose_name="Correo electronico cliente")
    logo = models.CharField(max_length=250, verbose_name="Logo", null=True)

    class Meta:
        db_table = 'cs_clients'

    def __str__(self):
        return f"{self.id}-{self.client_name}, {self.nit}"


# # ArrayField model
class Products(models.Model):
    """

    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=20, verbose_name="Tamaño o peso del producto")
    measure = models.CharField(max_length=5, default="gr", verbose_name="Unidad de medida")
    picture = models.CharField(max_length=250)
    pricing = models.IntegerField(default=0, verbose_name="Precio de venta")
    last_modify = models.DateField(default=now)

    class Meta:
        db_table = 'cs_products'
    """
    class Meta:
        abstract = True


class FormProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = (
            'code', 'name', 'size', 'picture', 'pricing', 'last_modify'
        )"""


class Attendant(models.Model):
    """

    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name="Nombre encargado")
    last_name = models.CharField(max_length=50, verbose_name="Apellido encargado")
    mobile = models.CharField(max_length=10, verbose_name="Celular encargado")
    note = models.CharField(max_length=200, verbose_name="Notas adicionales")

    class Meta:
        db_table = 'cs_attendant'


class Venues(models.Model):
    """

    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, verbose_name="Fijo corportativo")
    mobile = models.CharField(max_length=10, verbose_name="Celular corporativo")
    attendant = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    # products = ArrayField(model_container=Products, model_form_class=FormProduct, default=[])
    products = models.TextField(verbose_name="Lista de productos para esta sucursal")

    class Meta:
        db_table = 'cs_venues'


# # Marketing
class Marketing(models.Model):
    """
        Este es el mercadeo/venta
    """
    venue = models.ForeignKey(Venues, on_delete=models.CASCADE)
    init_date = models.DateField(default=now)
    deliver_date = models.DateField()
    purchase_order = models.CharField(max_length=50)
    order = models.CharField(max_length=200)
    notes = models.CharField(max_length=200, verbose_name="Notas adicionales")
    status = models.CharField(max_length=30, default="No entregado")

    class Meta:
        db_table = 'cd_marketing'


class StockByVenue(models.Model):
    """
        este dato lo llenaria el mercaderista
    """
    venue = models.ForeignKey(Venues, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    inventory = models.CharField(max_length=200)

    class Meta:
        db_table = 'cd_stock_by_venue'
