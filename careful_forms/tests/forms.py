from django.forms import CharField
from django.forms.forms import Form
from django.forms.models import ModelForm
from careful_forms.forms import CarefulForm, CarefulModelForm
from careful_forms.tests.models import SomeModel


class NormalForm(Form):
    name = CharField(max_length=200)
    email = CharField(max_length=200)
    dangerous_field = CharField(max_length=200)


class CarefullyfiedForm(CarefulForm):
    name = CharField(max_length=200)
    email = CharField(max_length=200)
    dangerous_field = CharField(max_length=200)


class NormalCorrectModelForm(ModelForm):
    class Meta:
        model = SomeModel
        exclude = ('dangerous_field_1', 'dangerous_field_2',)


class NormalIncorrectModelForm(ModelForm):
    class Meta:
        model = SomeModel
        exclude = ('dangerous_field_1',)


class CarefullyfiedCorrectModelForm(CarefulModelForm):
    class Meta:
        model = SomeModel
        exclude = ('dangerous_field_1', 'dangerous_field_2',)


class CarefullyfiedIncorrectModelForm(CarefulModelForm):
    class Meta:
        model = SomeModel
        exclude = ('dangerous_field_1', )
