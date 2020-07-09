from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import success
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.views.generic import TemplateView

from bill.decorators import unauthenticated_user
from bill.models import Client, Fournisseur
from login.forms import RegistrationForm


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome/')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login/login.html', context)


@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'successefully saved')
            user = form.save()

            group = request.POST.get("group")
            user.groups.add(group)
            print(group)
            if group == "0":
                client = Client(
                    user=user,
                    nom=request.POST.get("first_name"),
                    prenom=request.POST.get("last_name"),
                    adresse=request.POST.get("adresse"),
                    tel=request.POST.get("tel")

                )
                client = client.save()
            elif group == "1":
                fournisseur = Fournisseur(
                    user=user,
                    nom=request.POST.get("first_name"),
                    prenom=request.POST.get("last_name"),
                    adresse=request.POST.get("adresse"),
                    tel=request.POST.get("tel")

                )
                fournisseur = fournisseur.save()
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'login/register.html', {'form': form})
