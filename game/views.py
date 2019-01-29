from django.shortcuts import render

from django.shortcuts import render, redirect
from django import forms

from .models import QuantumCat, QuantumCats
from .qis_func import qiskit_catlapse
from .rand_ent import entangled_probs

IBM_Q = False

# Create your views here.
def index(request):
    num=8

    if request.method == "POST":
        boxed_cats = list(request.POST)
        boxed_cats.remove('csrfmiddlewaretoken')
        catchoices = ''
        if not(boxed_cats):
            catchoices = '0'*num
        else:
            for i in range(num):
                if str(i+1) in boxed_cats:
                    catchoices += '1'
                else:
                    catchoices += '0'
        QuantumCats = QuantumCats.objects.create(catchoices=catchoices)
        QuantumCats.save()
        return redirect('catlapse')

    probs, cov = entangled_probs(num)

    kitties = QuantumCat.objects
    entangled_kitties = []
    for id in probs:
        name = kitties.get(id=id+1).name
        prob = probs[id] * 10
        entangled_kitties.append((name, id+1, prob))
    context = {'entangled_kitties': entangled_kitties}
    return render(request, 'game/index.html', context)


def catlapse(request):
    latest_kitties = QuantumCats.objects.latest('id')
    catchoices = latest_kitties.catchoices

    catstatuses = qis_catlapse(catchoices, IBM_Q)

    kitties = QuantumCat.objects
    boxed_kitties = []
    for id in catstatuses:
        name = kitties.get(id=id+1).name
        boxed_kitties.append((name, catstatuses[id], id+1))

    context = {'boxed_kitties': boxed_kitties}
    return render(request, 'game/catlapse.html', context)


def entangle(request):
    context = {}
    return render(request, 'game/entangle.html', context)
