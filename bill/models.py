from django.contrib.auth.models import User
from django.db import models
import django_tables2 as tables
# Create your models here.

class Category(models.Model):
    nom         = models.CharField(max_length=120)

    def __str__(self):
        return self.nom
class Fournisseur(models.Model):
    """
    Model Fournisseur
    """
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, related_name="produits_forni")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.designation

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Client(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)


    def __str__(self):
        return self.nom + ' ' + self.prenom

class Order(models.Model):

    status = models.BooleanField(default=False, null=True)
    customer = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL,blank=True)
    date_order = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return  total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Produit,on_delete=models.SET_NULL,null=True,related_name='product')
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,related_name='orderitem_set')
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.prix * self.quantity
        return total
class ProductTable(tables.Table):
    action = '<a href= "{% url "product-delete" pk=record.id  %}" class ="btn btn-danger" > delete </a> '

    edit = tables.TemplateColumn(action)


    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"
        fields = ('designation','prix', 'fournisseur', 'category')

class LigneFournissTable(tables.Table):
    action = ' <a href= "{% url "fournisseur-delete" pk=record.id  %}" class ="btn btn-danger" > Supprimer </a> '

    edit = tables.TemplateColumn(action)


    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nom','prenom', 'adresse', 'tel')
class LigneClientTable(tables.Table):
    action = '<a href= "{% url "client-delete" pk=record.id  %}" class ="btn btn-danger" > Supprimer </a> '

    edit = tables.TemplateColumn(action)


    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nom','prenom', 'adresse', 'tel','chiffre_affaire')

class LigneCommandeTable(tables.Table):
    action = '<a href="{% url "commande-valider" pk=record.id  %}"    class ="btn btn-success  update-order" > valider </a>\
    <a href= "{% url "commande-delete" pk=record.id  %}" class ="btn btn-danger update-order" > Supprimer </a> '

    edit = tables.TemplateColumn(action)


    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap4.html"
        fields = ('customer','complete','get_cart_items','get_cart_total')