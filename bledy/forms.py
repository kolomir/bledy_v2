from django.forms import ModelForm
from django import forms
from .models import Klient, GrupaRobocza, Dzial, RodzajeBledu, Wiazka, Pracownik, Bledy, Csv, GrupaBledow, Lider_dzial, Karta


#= KARTA ===============================================================
class KartaForm(ModelForm):
    class Meta:
        model = Karta
        fields = [
            'nr_karty',
            'data_karty_miesiac',
            'data_karty_rok',
            'data_dodania',
            'wycofana'
        ]


#= LIDER - DZIAL =======================================================
class LiderDzial(ModelForm):
    class Meta:
        model = Lider_dzial
        fields = ['user','dzial']


#= KLIENCI =======================================================
class KlientForm(ModelForm):
    class Meta:
        model = Klient
        fields = ['nazwa_klienta','aktywny']


class SkasowacKlienci(ModelForm):
    class Meta:
        model = Klient
        fields = [
            'aktywny',
        ]


#= Grupa Błędów =======================================================
class GrupaBledowForm(ModelForm):
    class Meta:
        model = GrupaBledow
        fields = ['nazwa','aktywna']


class SkasowacGrupaBledow(ModelForm):
    class Meta:
        model = GrupaBledow
        fields = [
            'aktywna',
        ]


#= Grupa Robocza =======================================================
class GrupaRoboczaForm(ModelForm):
    class Meta:
        model = GrupaRobocza
        fields = ['nr_grupy','aktywna']


class SkasowacGrupaRobocza(ModelForm):
    class Meta:
        model = GrupaRobocza
        fields = [
            'aktywna',
        ]


#= Dział =======================================================
class DzialForm(ModelForm):
    class Meta:
        model = Dzial
        fields = ['dzial','aktywny']


class SkasowacDzial(ModelForm):
    class Meta:
        model = Dzial
        fields = [
            'aktywny',
        ]


#= Błąd =======================================================
class BladForm(ModelForm):
    class Meta:
        model = RodzajeBledu
        fields = ['blad','grupa_bledow','aktywny']


class SkasowacBlad(ModelForm):
    class Meta:
        model = RodzajeBledu
        fields = [
            'aktywny',
        ]


#= Wiązka =======================================================
class WiazkaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WiazkaForm, self).__init__(*args, **kwargs)
        self.fields['nazwa_klienta'] = forms.ModelChoiceField(queryset=Klient.objects.filter(aktywny=True))

    class Meta:
        model = Wiazka
        fields = ['nazwa_wiazki','nazwa_klienta','aktywny']


class SkasowacWiazka(ModelForm):
    class Meta:
        model = Wiazka
        fields = [
            'aktywny',
        ]


#= Pracownik =======================================================
class PracownikForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PracownikForm, self).__init__(*args, **kwargs)
        self.fields['dzial'] = forms.ModelChoiceField(queryset=Dzial.objects.filter(aktywny=True))

    class Meta:
        model = Pracownik
        fields = ['nr_pracownika','imie','nazwisko','dzial','zatrudniony']


class SkasowacPracownik(ModelForm):
    class Meta:
        model = Pracownik
        fields = [
            'zatrudniony',
        ]


#= Nowy błąd - wpis =======================================================
class BledyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BledyForm, self).__init__(*args, **kwargs)
        self.fields['nr_wiazki'] = forms.ModelChoiceField(queryset=Wiazka.objects.filter(aktywny=True))
        self.fields['nr_grupy_roboczej'] = forms.ModelChoiceField(queryset=GrupaRobocza.objects.filter(aktywna=True))
        self.fields['nr_budujacego'] = forms.ModelChoiceField(queryset=Pracownik.objects.filter(zatrudniony=True))
        self.fields['blad'] = forms.ModelChoiceField(queryset=RodzajeBledu.objects.filter(aktywny=True))

    class Meta:
        model = Bledy
        fields = [
            'nr_wiazki',
            'nr_grupy_roboczej',
            'nr_zlecenia',
            'nr_kontrolera',
            'nr_budujacego',
            'ilosc_skontrolowanych',
            'ilosc_bledow',
            'blad',
            'opis',
            'data_dodania'
        ]


class SkasowacBledy(ModelForm):
    class Meta:
        model = Bledy
        fields = [
            'skasowany',
        ]


class ZakonczycBledy(ModelForm):
    class Meta:
        model = Bledy
        fields = [
            'zakonczony',
        ]


# -- TEST CSV ------------------------------------------------
class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name',)


