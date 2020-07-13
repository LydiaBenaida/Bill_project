

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

    path('commande/', views.CommandeView.as_view(), name="commande-list"),
    path('commande/delete/<int:pk>', views.CommandeDelete, name="commande-delete"),
    path('commande/valider/<int:pk>', views.CommandeValider, name="commande-valider"),

    path('produit/facture/', views.FactureView.as_view(), name="facture"),

    path('produit/', views.ProductView.as_view(), name="produit"),
    path('produit/commande/delete/<int:pk>', views.ProductCommandeDelete.as_view(), name="commandeProduct-delete"),
    path('produit/commande/', views.ProductCommandeView.as_view(), name="commande"),
    path('produit/search/', views.SearchView, name="search"),

    path('produit/create/', views.ProductCreate.as_view(), name="product-create"),
    path('produit/delete/<int:pk>', views.ProductDeleteView.as_view(), name="product-delete"),
    path('category/', views.CategoryCreateView.as_view(), name="category"),

    path('fournisseur/', views.FournisseurView.as_view(), name="fournisseur-list"),
    path('fournisseur/delete/<int:pk>', views.FournisseurDeleteView.as_view(), name="fournisseur-delete"),

    path('clients/', views.ClientDetailView.as_view(), name="client-list"),
    path('clients/delete/<int:pk>', views.ClientDeleteView.as_view(), name="client-delete"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),

]
