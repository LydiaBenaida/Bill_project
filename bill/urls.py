

from django.contrib import admin
from django.urls import path

from bill import views

urlpatterns = [
    path('welcome/', views.welcome, name="welcome"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('updated_item/', views.updatedItem, name="update_item"),

    path('checkout/', views.checkout, name="checkout"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

    path('commande/', views.CommandeView, name="commande-list"),
    path('commande/delete/<int:pk>', views.CommandeDelete, name="commande-delete"),
    path('commande/valider/<int:pk>', views.CommandeValider, name="commande-valider"),

    path('produit/facture/', views.FactureView.as_view(), name="facture"),

    path('produit/', views.ProductView, name="produit"),
    path('produit/commande/delete/<int:pk>', views.ProductCommandeDelete.as_view(), name="commandeProduct-delete"),
    path('produit/commande/', views.ProductCommandeView.as_view(), name="commande"),
    path('produit/search/', views.SearchView, name="search"),
    path('produit/create/', views.ProductCreate, name="product-create"),
    path('produit/delete/<int:pk>', views.ProductDeleteView, name="product-delete"),
    path('category/', views.CategoryCreateView, name="category"),

    path('fournisseur/', views.FournisseurView, name="fournisseur-list"),
    path('fournisseur/delete/<int:pk>', views.FournisseurDeleteView, name="fournisseur-delete"),

    path('clients/', views.ClientDetailView, name="client-list"),
    path('clients/delete/<int:pk>', views.ClientDeleteView, name="client-delete"),
    path('dashboard/', views.DashboardView, name="dashboard"),

]
