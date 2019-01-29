from django.shortcuts import render

from django.shortcuts import render, redirect
from django import forms

from .models import QuantumCat, QuantumCats
from .qiskit import get_catlapse, get_catangle

IBM_Q = False

# Create your views here.
def index(request):
    num=8

    if request.method == "POST":
        boxed_cats = list(request.POST)
        boxed_cats.remove('csrfmiddlewaretoken')
        cat_choices = ''
        if not(boxed_cats):
            cat_choices = '0'*num
        else:
            for i in range(num):
                if str(i+1) in boxed_cats:
                    cat_choices += '1'
                else:
                    cat_choices += '0'
        cat = QuantumCats.objects.create(cat_choices=cat_choices)
        cat.save()
        return redirect('catlapse')

    probs, cov = get_catangle(num)

    cats = QuantumCat.objects
    entangled_cats = []
    for id in probs:
        name = cats.get(id=id+1).name
        prob = probs[id] * 10
        entangled_cats.append((name, id+1, prob))
    context = {'entangled_cats': entangled_cats}
    return render(request, 'game/index.html', context)


def catlapse(request):
    latest_cats = QuantumCats.objects.latest('id')
    cat_choices = latest_cats.cat_choices

    cat_statuses = get_catlapse(cat_choices, IBM_Q)

    cats = QuantumCat.objects
    boxed_cats = []
    for id in cat_statuses:
        name = cats.get(id=id+1).name
        boxed_cats.append((name, cat_statuses[id], id+1))

    context = {'boxed_cats': boxed_cats}
    return render(request, 'game/catlapse.html', context)


def entangle(request):
    context = {}
    return render(request, 'game/entangle.html', context)
