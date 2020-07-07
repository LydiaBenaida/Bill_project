# Generated by Django 3.0.5 on 2020-05-29 10:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=50, null=True)),
                ('prenom', models.CharField(blank=True, max_length=50, null=True)),
                ('adresse', models.TextField(blank=True, null=True)),
                ('tel', models.CharField(blank=True, max_length=10, null=True)),
                ('sexe', models.CharField(choices=[('M', 'Masculin'), ('F', 'Feminin')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billApp.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=50, null=True)),
                ('prenom', models.CharField(blank=True, max_length=50, null=True)),
                ('adresse', models.TextField(blank=True, null=True)),
                ('tel', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50)),
                ('prix', models.FloatField(default=0)),
                ('fournisseur', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='billApp.Fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='LigneFacture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte', models.IntegerField(default=1)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes', to='billApp.Facture')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billApp.Produit')),
            ],
        ),
        migrations.AddConstraint(
            model_name='lignefacture',
            constraint=models.UniqueConstraint(fields=('produit', 'facture'), name='produit-facture'),
        ),
    ]
