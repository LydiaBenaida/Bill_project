import json
from pickle import GET
from webbrowser import get

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, fields, F, ExpressionWrapper
from django.http import JsonResponse, request
from django.shortcuts import render

from . import tables, charts
# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Button

from bill import models
from bill.decorators import allowed_users
from bill.models import Produit, Order, Client, OrderItem, Category, ProductTable, Fournisseur, LigneFournissTable, \
    LigneClientTable, LigneCommandeTable, ProductCommandeTable, FactureTable
from django_tables2.config import RequestConfig


from django_tables2 import SingleTableView

@login_required(login_url='login/')
def welcome(request):
    context = {}
    return render(request, 'bill/base.html', context)




@allowed_users(allowed_roles=['client'])
def store(request):
    if request.user.is_authenticated:
        customer = request.user.client
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems=order['get_cart_items']
    products = Produit.objects.all()
    context = {'items':items,'products':products,'cartItems':cartItems}
    return render(request, 'bill/store.html', context)

@allowed_users(allowed_roles=['client'])
def SearchView(request):



    if request.user.is_authenticated:
        customer = request.user.client
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
        try:
            q = request.GET.get('q')
        except:
            q = None
        if q:
            products = Produit.objects.filter(designation__icontains=q)
    else:
        try:
            q = request.GET.get('q')
        except:
            q = None
        if q:
            products = Produit.objects.filter(designation__icontains=q)



        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems=order['get_cart_items']

    context = {'items':items,'products':products,'cartItems':cartItems}
    return render(request, 'bill/store.html', context)

@allowed_users(allowed_roles=['client'])
def cart(request):

    if request.user.is_authenticated:
        customer = request.user.client
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    messages.success(request, 'successefully saved')
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'bill/cart.html', context)

@allowed_users(allowed_roles=['client'])
def checkout(request):

    customer  = request.user.client
    order = Order.objects.get(customer=customer, complete=False)
    order.complete=True
    order.save()


    context = {}
    return render(request, 'bill/base.html', context)


@allowed_users(allowed_roles=['client'])
def updatedItem(request):
    data= json.loads(request.body)
    product=data['product']
    action=data['action']
    messages.success(request, 'added successefully ')
    print('product',product,'action',action)
    customer=request.user.client
    product=Produit.objects.get(id=product)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action =='add':
        orderItem.quantity =(orderItem.quantity+1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was addes',safe=False)

class LogoutView(TemplateView):

  template_name = 'login/login.html'

  def get(self, request, **kwargs):

    logout(request)

    return render(request, self.template_name)


class CategoryCreateView(CreateView):
  model = Category
  template_name = 'bill/create.html'
  fields = ['nom']

  def get_form(self, form_class=None):
      form = super().get_form(form_class)
      form.helper = FormHelper()
     # messages.success(request, 'successefully added')
      form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
      form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
      return form

  def get_success_url(self):
      return f"/category/"


class ProductView(SingleTableView):
    template_name = 'bill/list_product.html'
    model = Produit

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)

        table = ProductTable(Produit.objects.all())
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context


class ProductDeleteView(DeleteView):
    model = Produit
    template_name = 'bill/delete.html'


    def get_success_url(self):
        return f"/produit/"


class ProductCreate(CreateView):
    model = models.Produit
    fields = ["designation", "prix","fournisseur","category","image"]
    template_name = "bill/create.html"

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        context["object_name"] = "Product"
        return context

    def get_success_url(self):
        return f"/produit/"



class ProductCommandeDelete(DeleteView):
    model = Order
    template_name = 'bill/delete.html'

    def get_success_url(self):
        return f"/produit/commande/"

class ProductCommandeView(SingleTableView):
    template_name = 'bill/list.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(ProductCommandeView, self).get_context_data(**kwargs)

        table = ProductCommandeTable(Order.objects.filter(status=False,complete=True))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context
class FactureView(SingleTableView):
    template_name = 'bill/list.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(FactureView, self).get_context_data(**kwargs)

        table = FactureTable(Order.objects.filter(status=True))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context


class ClientDetailView(SingleTableView):
    template_name = 'bill/list.html'
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)

        table = LigneClientTable(Client.objects.all().annotate(
            chiffre_affaire=Sum(ExpressionWrapper(F('order__orderitem_set__quantity')*F('order__orderitem_set__product__prix'),
                                                  output_field=fields.FloatField()))))

        context['table'] = table
        return context




class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'bill/delete.html'

    def get_success_url(self):
        return f"/clients/"



class FournisseurView(SingleTableView):
    template_name = 'bill/list.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(FournisseurView, self).get_context_data(**kwargs)

        table = LigneFournissTable(Fournisseur.objects.all())
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context

class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    template_name = 'bill/delete.html'

    def get_success_url(self):
        return f"/fournisseur/"


class CommandeView(SingleTableView):
    template_name = 'bill/list.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(CommandeView, self).get_context_data(**kwargs)

        table = LigneCommandeTable(Order.objects.filter(complete=True,status=False))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context
@allowed_users(allowed_roles=['admin'])

def CommandeDelete(request,pk):
    order = Order.objects.get(id=pk)
    order.status = False
    order.save()

    context = {}
    return render(request, 'bill/base.html', context)

@allowed_users(allowed_roles=['admin'])

def CommandeValider(request,pk):

    order = Order.objects.get(id=pk)
    order.status = True
    order.save()

    context = {}
    return render(request, 'bill/dashboard.html', context)


class DashboardView(TemplateView):

    template_name = "bill/dashboard.html"

    def get_context_data(self,**kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        fournisseur_qs  = models.Fournisseur.objects.annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('produits_forni__product__quantity') * F('produits_forni__prix'),
                output_field=fields.FloatField()
            )
        ))

        client_qs       = models.Client.objects.annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('order__orderitem_set__quantity') * F('order__orderitem_set__product__prix'),
                output_field=fields.FloatField()
            )
        )).order_by("-chiffre_affaire")

        context["fournisseur_table"]    = tables.FournisseurWithChiffreAffaireTable(fournisseur_qs)
        context["client_table"]         = tables.ClientWithChiffreAffaireTable(client_qs)
        context["daily_stat"]           = charts.DailyStatChart()
        context["category_stat"]        = charts.CategoryStatChart()
        return context
