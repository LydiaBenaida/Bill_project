from django.db.models import Avg, Count, Min, Sum,ExpressionWrapper,fields,F
from .models import Order, Category
from jchart import Chart
from jchart.config import DataSet

class DailyStatChart(Chart):
    chart_type = 'line'
    qs = Order.objects.values('date_order').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('orderitem_set__quantity') * F('orderitem_set__product__prix'),
                output_field=fields.FloatField()
            )
        ))
    
    def get_datasets(self, **kwargs):
        
        return [DataSet(
            color=(60, 170, 20),
            data=list(self.qs.values_list('chiffre_affaire',flat=True)),
            label="l'évolution du chiffre d'affaire"
            )]

    def get_labels(self, **kwargs):
        return list(self.qs.values_list('date_order',flat=True))

class CategoryStatChart(Chart):
    chart_type = 'radar'
    qs = Category.objects.values('nom').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(
                F('produit__product__quantity') * F('produit__prix'),
                output_field=fields.FloatField()
            )
        ))
    
    def get_datasets(self, **kwargs):
        
        return [DataSet(
            color=(245, 66, 170), 
            data=list(self.qs.values_list('chiffre_affaire',flat=True)),
            label="chiffre d'affaire par Categorie"
            )]

    def get_labels(self, **kwargs):
        return list(self.qs.values_list('nom',flat=True))