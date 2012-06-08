from django.shortcuts import render
from careful_forms.tests.forms import (
    NormalForm, CarefullyfiedIncorrectModelForm, CarefullyfiedCorrectModelForm
)


def normal_form(request):
    return render(request, "form.html", {'form': NormalForm()})


def careful_incorrect_model_form(request):
    return render(request, "form.html", {'form': CarefullyfiedIncorrectModelForm()})


def careful_correct_model_form(request):
    return render(request, "form.html", {'form': CarefullyfiedCorrectModelForm()})
