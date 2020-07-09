from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Category)
admin.site.register(Produit)

admin.site.register(Fournisseur)
admin.site.register(Client)

admin.site.register(Order)
admin.site.register(OrderItem)