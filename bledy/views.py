from django.shortcuts import render, get_object_or_404, redirect
from .models import Bledy, Klient, GrupaRobocza, Dzial, RodzajeBledu, Wiazka, Pracownik, Autor, RodzajReklamacji, Csv, GrupaBledow, Lider_dzial, Karta
from .forms import KlientForm, SkasowacKlienci, GrupaRoboczaForm, SkasowacGrupaRobocza, DzialForm, SkasowacDzial, \
                BladForm, SkasowacBlad, WiazkaForm, SkasowacWiazka, PracownikForm, SkasowacPracownik, BledyForm, \
                SkasowacBledy, CsvModelForm, GrupaBledowForm, SkasowacGrupaBledow, LiderDzial, KartaForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model


def get_author(user):
    qs = Autor.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def ostatnie_wpisy(request):
    wszystkie_wpisy = Bledy.objects.filter(skasowany=False).order_by('-id')[:300]
    karta = Karta.objects.filter(wycofana=False).order_by('-id')[:200]

    if request.user.is_authenticated:
        zglaszajacy_wpisy = get_author(request.user)
        lista_userow = get_user_model()
        autor_wpisu = get_object_or_404(lista_userow, username__exact=zglaszajacy_wpisy)
        lista_autors = Autor.objects.filter(user_id=autor_wpisu.id).values_list('id',flat=True)
        id_autor = lista_autors[0]

        zalogowany_user = request.user
        zalogowany_user_id = request.user.id

        dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
        lider_grupa = int(dostepy.lider)
        kontrol_grupa = int(dostepy.kontrol)
        jakosc_grupa = int(dostepy.jakosc)

        department_ids = Lider_dzial.objects.filter(user_id=zalogowany_user_id).values_list('dzial_id', flat=True)
        wpisy_lider = Bledy.objects.filter(nr_grupy_roboczej__in=department_ids).filter(zakonczony=0).filter(skasowany=0).select_related('nr_karty')
        karta_wpis = Bledy.objects.filter(nr_karty__in=karta).filter(zakonczony=0)
    else:
        zalogowany_user = ""
        zalogowany_user_id = ""
        department_ids = ""
        wpisy_lider = ""
        id_autor = ""
        lider_grupa = ''
        kontrol_grupa = ''
        jakosc_grupa = ''

    context = {
        'wszystkie_wpisy': wszystkie_wpisy,
        'wpisy_lider': wpisy_lider,
        'zalogowany_user_id': zalogowany_user_id,
        'zalogowany_user': zalogowany_user,
        'id_autor': id_autor,
        'karta': karta,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }

    return render(request, 'bledy/ostatnie_wpisy.html', context)


def wszystkie_wpisy(request):
    wszystkie_wpisy = Bledy.objects.order_by('-id')

    if request.user.is_authenticated:
        zglaszajacy_wpisy = get_author(request.user)
        lista_userow = get_user_model()
        autor_wpisu = get_object_or_404(lista_userow, username__exact=zglaszajacy_wpisy)
        lista_autors = Autor.objects.filter(user_id=autor_wpisu.id).values_list('id', flat=True)
        id_autor = lista_autors[0]

        zalogowany_user = request.user
        zalogowany_user_id = request.user.id

        dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
        lider_grupa = int(dostepy.lider)
        kontrol_grupa = int(dostepy.kontrol)
        jakosc_grupa = int(dostepy.jakosc)

    context = {
        'wszystkie_wpisy': wszystkie_wpisy,
        'zalogowany_user_id': zalogowany_user_id,
        'zalogowany_user': zalogowany_user,
        'id_autor': id_autor,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }

    return render(request, 'bledy/wszystkie_wpisy.html', context)



@login_required
def przypisz_lider_dzial(request):
    form_lider_dzial = LiderDzial(request.POST or None, request.FILES or None)
    lider_user = Autor.objects.all()
    grupa = GrupaRobocza.objects.filter(aktywna=True).order_by('nr_grupy')

    if form_lider_dzial.is_valid():
        get_lider = request.POST.get('lider_user')
        form_lider_dzial.save()
        return redirect(wpisy_lider_dzial)

    context = {
        'form_lider_dzial': form_lider_dzial,
        'lider_user': lider_user,
        'grupa': grupa,
    }

    return render(request, 'bledy/form_lider_dzial.html', context)


def wpisy_lider_dzial(request):
    lider_dzial = Lider_dzial.objects.all().order_by('user')

    zalogowany_user = request.user
    dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    lider_grupa = int(dostepy.lider)
    kontrol_grupa = int(dostepy.kontrol)
    jakosc_grupa = int(dostepy.jakosc)

    context = {
        'lider_dzial': lider_dzial,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }
    return render(request,'bledy/lider_dzial.html',context)


@login_required
def nowy_klient(request):
    form_klienci = KlientForm(request.POST or None, request.FILES or None)

    if form_klienci.is_valid():
        form_klienci.save()
        return redirect(wpisyKlient)

    context = {
        'form_klienci': form_klienci
    }

    return render(request, 'bledy/form_klient.html', context)


@login_required
def edytuj_klient(request, id):
    wpis = get_object_or_404(Klient, pk=id)

    form_klienci = KlientForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_klienci.is_valid():
        form_klienci.save()
        return redirect(wpisyKlient)

    context = {
        'form_klienci': form_klienci,
        'wpis': wpis
    }

    return render(request, 'bledy/form_klient_ed.html', context)


@login_required
def usun_klient(request, id):
    wpis = get_object_or_404(Klient, pk=id)
    form_wpis = SkasowacKlienci(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywny = 0
        kasuj.save()
        return redirect(wpisyKlient)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_klient.html', context)


@login_required
def przywroc_klient(request, id):
    wpis = get_object_or_404(Klient, pk=id)
    form_wpis = SkasowacKlienci(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywny = 1
        kasuj.save()
        return redirect(wpisyKlient)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_klient.html', context)


def wpisyKlient(request):
    klienci = Klient.objects.all().order_by('nazwa_klienta')

    zalogowany_user = request.user
    dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    lider_grupa = int(dostepy.lider)
    kontrol_grupa = int(dostepy.kontrol)
    jakosc_grupa = int(dostepy.jakosc)

    context = {
        'klienci': klienci,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }
    return render(request,'bledy/klienci.html',context)


@login_required
def nowa_grupa_bledow(request):
    form_grupy_bledow = GrupaBledowForm(request.POST or None, request.FILES or None)

    if form_grupy_bledow.is_valid():
        form_grupy_bledow.save()
        return redirect(wpisyGrupaBledow)

    context = {
        'form_grupy_bledow': form_grupy_bledow
    }

    return render(request, 'bledy/form_grupa_bledow.html', context)


@login_required
def edytuj_grupa_bledow(request, id):
    wpis = get_object_or_404(GrupaBledow, pk=id)

    form_grupy_bledow = GrupaBledowForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_grupy_bledow.is_valid():
        form_grupy_bledow.save()
        return redirect(wpisyGrupaBledow)

    context = {
        'form_grupy_bledow': form_grupy_bledow,
        'wpis': wpis
    }

    return render(request, 'bledy/form_grupa_bledow_ed.html', context)


@login_required
def usun_grupa_bledow(request, id):
    wpis = get_object_or_404(GrupaBledow, pk=id)
    form_wpis = SkasowacGrupaBledow(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywna = 0
        kasuj.save()
        return redirect(wpisyGrupaBledow)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_grupa_bledow.html', context)


@login_required
def przywroc_grupa_bledow(request, id):
    wpis = get_object_or_404(GrupaBledow, pk=id)
    form_wpis = SkasowacGrupaBledow(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywna = 1
        kasuj.save()
        return redirect(wpisyGrupaBledow)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_grupa_bledow.html', context)


def wpisyGrupaBledow(request):
    grupy_bledow = GrupaBledow.objects.all().order_by('nazwa')

    zalogowany_user = request.user
    dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    lider_grupa = int(dostepy.lider)
    kontrol_grupa = int(dostepy.kontrol)
    jakosc_grupa = int(dostepy.jakosc)

    context = {
        'grupy_bledow': grupy_bledow,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }
    return render(request, 'bledy/grupybledow.html', context)


@login_required
def nowa_grupa(request):
    form_grupy = GrupaRoboczaForm(request.POST or None, request.FILES or None)

    if form_grupy.is_valid():
        form_grupy.save()
        return redirect(wpisyGrupaRobocza)

    context = {
        'form_grupy': form_grupy
    }

    return render(request, 'bledy/form_grupa.html', context)


@login_required
def edytuj_grupa(request, id):
    wpis = get_object_or_404(GrupaRobocza, pk=id)

    form_grupy = GrupaRoboczaForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_grupy.is_valid():
        form_grupy.save()
        return redirect(wpisyGrupaRobocza)

    context = {
        'form_grupy': form_grupy,
        'wpis': wpis
    }

    return render(request, 'bledy/form_grupa_ed.html', context)


@login_required
def usun_grupa(request, id):
    wpis = get_object_or_404(GrupaRobocza, pk=id)
    form_wpis = SkasowacGrupaRobocza(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywna = 0
        kasuj.save()
        return redirect(wpisyGrupaRobocza)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_grupa.html', context)


@login_required
def przywroc_grupa(request, id):
    wpis = get_object_or_404(GrupaRobocza, pk=id)
    form_wpis = SkasowacGrupaRobocza(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywna = 1
        kasuj.save()
        return redirect(wpisyGrupaRobocza)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_grupa.html', context)


def wpisyGrupaRobocza(request):
    grupy_robocze = GrupaRobocza.objects.all().order_by('nr_grupy')

    zalogowany_user = request.user
    dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    lider_grupa = int(dostepy.lider)
    kontrol_grupa = int(dostepy.kontrol)
    jakosc_grupa = int(dostepy.jakosc)

    context = {
        'grupy_robocze': grupy_robocze,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }
    return render(request, 'bledy/grupyrobocze.html', context)


@login_required
def nowy_dzial(request):
    form_dzial = DzialForm(request.POST or None, request.FILES or None)

    if form_dzial.is_valid():
        form_dzial.save()
        return redirect(wpisyDzialy)

    context = {
        'form_dzial': form_dzial
    }

    return render(request, 'bledy/form_dzial.html', context)


@login_required
def edytuj_dzial(request, id):
    wpis = get_object_or_404(Dzial, pk=id)

    form_dzial = DzialForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_dzial.is_valid():
        form_dzial.save()
        return redirect(wpisyDzialy)

    context = {
        'form_dzial': form_dzial,
        'wpis': wpis
    }

    return render(request, 'bledy/form_dzial_ed.html', context)


@login_required
def usun_dzial(request, id):
    wpis = get_object_or_404(Dzial, pk=id)
    form_wpis = SkasowacDzial(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywny = 0
        kasuj.save()
        return redirect(wpisyDzialy)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_dzial.html', context)


@login_required
def przywroc_dzial(request, id):
    wpis = get_object_or_404(Dzial, pk=id)
    form_wpis = SkasowacDzial(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywny = 1
        kasuj.save()
        return redirect(wpisyDzialy)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_dzial.html', context)


def wpisyDzialy(request):
    dzialy = Dzial.objects.all().order_by('dzial')

    zalogowany_user = request.user
    dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    lider_grupa = int(dostepy.lider)
    kontrol_grupa = int(dostepy.kontrol)
    jakosc_grupa = int(dostepy.jakosc)

    context = {
        'dzialy': dzialy,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }
    return render(request,'bledy/dzialy.html',context)


@login_required
def nowy_blad(request):
    form_blad = BladForm(request.POST or None, request.FILES or None)
    grupa_bledow = GrupaBledow.objects.filter(aktywna=True).order_by('nazwa')

    if form_blad.is_valid():
        bl = request.GET.get('blad')
        gr = request.GET.get('grupa_bledow')
        form_blad.save()
        return redirect(wpisyBlad)

    context = {
        'form_blad': form_blad,
        'grupa_bledow': grupa_bledow
    }

    return render(request, 'bledy/form_bledy.html', context)


@login_required
def edytuj_blad(request, id):
    wpis = get_object_or_404(RodzajeBledu, pk=id)
    grupa_bledow = GrupaBledow.objects.filter(aktywna=True).order_by('nazwa')

    form_blad = BladForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_blad.is_valid():
        form_blad.save()
        return redirect(wpisyBlad)

    context = {
        'form_blad': form_blad,
        'grupa_bledow': grupa_bledow,
        'wpis': wpis
    }

    return render(request, 'bledy/form_bledy_ed.html', context)


@login_required
def usun_blad(request, id):
    wpis = get_object_or_404(RodzajeBledu, pk=id)
    form_wpis = SkasowacBlad(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywny = 0
        kasuj.save()
        return redirect(wpisyBlad)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_blad.html', context)


@login_required
def przywroc_blad(request, id):
    wpis = get_object_or_404(RodzajeBledu, pk=id)
    form_wpis = SkasowacBlad(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywny = 1
        kasuj.save()
        return redirect(wpisyBlad)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_blad.html', context)


def wpisyBlad(request):
    bledy = RodzajeBledu.objects.all().order_by('blad')

    zalogowany_user = request.user
    dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    lider_grupa = int(dostepy.lider)
    kontrol_grupa = int(dostepy.kontrol)
    jakosc_grupa = int(dostepy.jakosc)

    context = {
        'bledy': bledy,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }
    return render(request, 'bledy/bledy.html', context)


@login_required
def nowa_wiazka(request):
    form_wiazka = WiazkaForm(request.POST or None, request.FILES or None)
    klient = Klient.objects.filter(aktywny=True).order_by('nazwa_klienta')

    if form_wiazka.is_valid():
        form_wiazka.save()
        return redirect(wpisyWiazka)

    context = {
        'form_wiazka': form_wiazka,
        'klient': klient
    }

    return render(request, 'bledy/form_wiazka.html', context)


@login_required
def edytuj_wiazka(request, id):
    wpis = get_object_or_404(Wiazka, pk=id)
    klient = Klient.objects.filter(aktywny=True).order_by('nazwa_klienta')

    form_wiazka = WiazkaForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_wiazka.is_valid():
        form_wiazka.save()
        return redirect(wpisyWiazka)

    context = {
        'form_wiazka': form_wiazka,
        'wpis': wpis,
        'klient': klient
    }

    return render(request, 'bledy/form_wiazka_ed.html', context)


@login_required
def usun_wiazke(request, id):
    wpis = get_object_or_404(Wiazka, pk=id)
    form_wpis = SkasowacWiazka(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywny = 0
        kasuj.save()
        return redirect(wpisyWiazka)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_wiazka.html', context)


@login_required
def przywroc_wiazke(request, id):
    wpis = get_object_or_404(Wiazka, pk=id)
    form_wpis = SkasowacWiazka(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.aktywny = 1
        kasuj.save()
        return redirect(wpisyWiazka)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_wiazka.html', context)


def wpisyWiazka(request):
    wiazka = Wiazka.objects.all().order_by('nazwa_wiazki')

    zalogowany_user = request.user
    dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    lider_grupa = int(dostepy.lider)
    kontrol_grupa = int(dostepy.kontrol)
    jakosc_grupa = int(dostepy.jakosc)

    context = {
        'wiazka': wiazka,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }
    return render(request,'bledy/wiazka.html',context)


@login_required
def nowy_pracownik(request):
    form_pracownik = PracownikForm(request.POST or None, request.FILES or None)
    dzial = Dzial.objects.filter(aktywny=True).order_by('dzial')

    if form_pracownik.is_valid():
        form_pracownik.save()
        return redirect(wpisyPracownik)

    context = {
        'form_pracownik': form_pracownik,
        'dzial': dzial
    }

    return render(request, 'bledy/form_pracownik.html', context)


@login_required
def edytuj_pracownik(request, id):
    wpis = get_object_or_404(Pracownik, pk=id)
    dzial = Dzial.objects.filter(aktywny=True).order_by('dzial')
    form_pracownik = PracownikForm(request.POST or None, request.FILES or None, instance=wpis)

    if form_pracownik.is_valid():
        form_pracownik.save()
        return redirect(wpisyPracownik)

    context = {
        'form_pracownik': form_pracownik,
        'wpis': wpis,
        'dzial': dzial
    }

    return render(request, 'bledy/form_pracownik_ed.html', context)


@login_required
def usun_pracownik(request, id):
    wpis = get_object_or_404(Pracownik, pk=id)
    form_wpis = SkasowacPracownik(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.zatrudniony = 0
        kasuj.save()
        return redirect(wpisyPracownik)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_pracownik.html', context)


@login_required
def przywroc_pracownik(request, id):
    wpis = get_object_or_404(Pracownik, pk=id)
    form_wpis = SkasowacPracownik(request.POST or None, request.FILES or None, instance=wpis)

    if form_wpis.is_valid():
        kasuj = form_wpis.save(commit=False)
        kasuj.zatrudniony = 1
        kasuj.save()
        return redirect(wpisyPracownik)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_pracownik.html', context)


def wpisyPracownik(request):
    pracownik = Pracownik.objects.all().order_by('nr_pracownika')

    zalogowany_user = request.user
    dostepy = get_object_or_404(Autor, user_id__exact=zalogowany_user.id)
    lider_grupa = int(dostepy.lider)
    kontrol_grupa = int(dostepy.kontrol)
    jakosc_grupa = int(dostepy.jakosc)

    context = {
        'pracownik': pracownik,
        'lider_grupa': lider_grupa,
        'kontroler_grupa': kontrol_grupa,
        'jakosc_grupa': jakosc_grupa,
    }
    return render(request,'bledy/pracownik.html',context)


@login_required
def nowy_blad_wpis(request):
    form_blad_wpis = BledyForm(request.POST or None, request.FILES or None)
    grupa = GrupaRobocza.objects.filter(aktywna=True).order_by('nr_grupy')
    budujacy = Pracownik.objects.filter(zatrudniony=True).order_by('nr_pracownika')
    rodzajBledu = RodzajeBledu.objects.filter(aktywny=True).order_by('blad')

    # - DANE Z SESJI -----------------------
    karta_id = request.session['karta_id']
    karta_id_table = get_object_or_404(Karta, pk=karta_id)
    kolejny = request.session['kolejny']
    nr_grupy_roboczej_id = request.session['nr_grupy_roboczej_id']
    nr_grupy_roboczej = request.session['nr_grupy_roboczej']
    nr_budujacego_id = request.session['nr_budujacego_id']
    budujacy_nazwisko = request.session['budujacy_nazwisko']
    budujacy_imie = request.session['budujacy_imie']
    budujacy_nr = request.session['budujacy_nr']
    nr_grupy_roboczej_id1 = request.POST.get('nr_grupy_roboczej')
    nr_budujacego1 = request.POST.get('nr_budujacego')
    blad1 = request.POST.get('nr_budujacego')
    data_dodania1 = request.POST.get('data_dodania')

    # - NIECZYNNE KOLUMNY - dane -------
    wiazka = 1
    skontrolowanych = 1
    zlecenie = 1

    print('-- Pre Product ---------------------')
    print('karta_id: ', karta_id)
    print('karta_id_table: ', karta_id_table.id)

    moja_Data = datetime.now()
    data_dodania = moja_Data.strftime("%Y-%m-%d")

    if request.method == 'POST' and 'zapisz_i_koniec' in request.POST:
        if form_blad_wpis.is_valid():
            instancja = form_blad_wpis.save(commit=False)
            autor = get_author(request.user)
            instancja.autor_wpisu = autor
            instancja.nr_karty = karta_id_table
            request.session['kolejny'] = 'nie'

            # - NIECZYNNE KOLUMNY --------------------
            instancja.ilosc_skontrolowanych = skontrolowanych
            instancja.nr_zlecenia = zlecenie
            instancja.nr_wiazki_id = wiazka

            instancja.save()
            return redirect(ostatnie_wpisy)
        else:
            form_blad_wpis.errors

    if request.method == 'POST' and 'zapisz_i_dodaj' in request.POST:
        # - odczyt i przygotowanie danych ----------------------
        nr_grupy_roboczej_id = request.POST.get('nr_grupy_roboczej')
        wyb_grupy_roboczej = GrupaRobocza.objects.filter(id=nr_grupy_roboczej_id)
        nr_grupy_roboczej = str(wyb_grupy_roboczej[0])

        nr_budujacego_id = request.POST.get('nr_budujacego')
        budujacy = Pracownik.objects.filter(id=nr_budujacego_id)
        budujacy_nazwisko = str(budujacy[0].nazwisko)
        budujacy_imie = str(budujacy[0].imie)
        budujacy_nr = str(budujacy[0])

        if form_blad_wpis.is_valid():
            instancja = form_blad_wpis.save(commit=False)
            autor = get_author(request.user)
            instancja.autor_wpisu = autor
            karta_id = request.POST.get('id_karty')
            instancja.nr_karty = karta_id_table
            request.session['kolejny'] = 'tak'

            # - NIECZYNNE KOLUMNY --------------------
            instancja.ilosc_skontrolowanych = skontrolowanych
            instancja.nr_zlecenia = zlecenie
            instancja.nr_wiazki_id = wiazka

            instancja.save()

            # - DANE DO SESJI --------------------
            request.session['nr_grupy_roboczej_id'] = nr_grupy_roboczej_id
            request.session['nr_grupy_roboczej'] = nr_grupy_roboczej
            request.session['nr_budujacego_id'] = nr_budujacego_id
            request.session['budujacy_nazwisko'] = budujacy_nazwisko
            request.session['budujacy_imie'] = budujacy_imie
            request.session['budujacy_nr'] = budujacy_nr

            return redirect(nowy_blad_wpis)
        else:
            form_blad_wpis.errors

    context = {
        'form_blad_wpis': form_blad_wpis,
        'grupa': grupa,
        'budujacy': budujacy,
        'rodzajBledu': rodzajBledu,
        'id_karty': karta_id,
        'data_dodania': data_dodania,
        'kolejny': kolejny,
        'nr_grupy_roboczej_id': nr_grupy_roboczej_id,
        'nr_grupy_roboczej': nr_grupy_roboczej,
        'nr_budujacego_id': nr_budujacego_id,
        'budujacy_nazwisko': budujacy_nazwisko,
        'budujacy_imie': budujacy_imie,
        'budujacy_nr': budujacy_nr,
    }

    return render(request, 'bledy/form_bledy_wpisy.html', context)


def wpisyKarta(request):
    karta = Karta.objects.all().order_by('-id')

    context = {
        'karta': karta
    }
    return render(request,'bledy/wszystkie_karty.html',context)


@login_required
def nowaKarta(request):
    form_karta = KartaForm(request.POST or None, request.FILES or None)
    wiazka = Wiazka.objects.filter(aktywny=True).order_by('nazwa_wiazki')
    #karta = Karta.objects.all().order_by('-id')[:30]
    ostatni_wpis = Karta.objects.latest('id')

    moja_Data = datetime.now()
    data_dodania = moja_Data.strftime("%Y-%m-%d")
    data_dodania_miesiac = int(moja_Data.strftime("%m"))
    data_dodania_rok = int(moja_Data.strftime("%Y"))
    nr_karty = int(ostatni_wpis.id) + 1
    wycofana = False

    #- NIECZYNNE KOLUMNY - dane -------
    karta_nrKarty = 1

    print('-- Karta ---------------------')
    print('ostatni_wpis: ', ostatni_wpis.id)
    print('nr_karty: ', nr_karty)

    if request.method == 'POST':
        if form_karta.is_valid():
            dopisz = form_karta.save(commit=False)
            autor = get_author(request.user)
            nr_wiazki_id = request.POST.get('nr_wiazki')
            nr_zlecenia = request.POST.get('nr_zlecenia')
            ilosc_wadliwych = request.POST.get('ilosc_wadliwych')
            zolta_we = request.POST.get('zolta')
            nr_karty = request.POST.get('nr_karty')
            if zolta_we == 'on':
                zolta = True
            else:
                zolta = False

            # - NIECZYNNE KOLUMNY --------------------
            dopisz.nr_karty = int(karta_nrKarty)

            # - WŁAŚCIWE DANE --------------------
            dopisz.data_karty_miesiac = data_dodania_miesiac
            dopisz.data_karty_rok = data_dodania_rok
            dopisz.wycofana = 0
            dopisz.nr_wiazki_id = int(nr_wiazki_id)
            dopisz.nr_zlecenia = nr_zlecenia
            dopisz.ilosc_wadliwych = ilosc_wadliwych
            dopisz.autor_wpisu = autor
            dopisz.zolta = zolta
            dopisz.save()

            # - DANE DO SESJI --------------------
            request.session['karta_id'] = nr_karty
            request.session['kolejny'] = 'nie'
            request.session['nr_grupy_roboczej_id'] = 0
            request.session['nr_grupy_roboczej'] = 'nic'
            request.session['nr_budujacego_id'] = 0
            request.session['budujacy_nazwisko'] = 'nic'
            request.session['budujacy_imie'] = 'nic'
            request.session['budujacy_nr'] = 'nic'
            request.session['zolta'] = False
            return redirect(nowy_blad_wpis)
        else:
            print('Nie jest VALID!')
            print('Error: ',form_karta.errors)
    else:
        print('Coś nie tak!')

    context = {
        'form_karta': form_karta,
        'data_dodania': data_dodania,
        'data_dodania_miesiac': str(data_dodania_miesiac),
        'data_dodania_rok': str(data_dodania_rok),
        'nr_karty': int(nr_karty),
        'wycofana': wycofana,
        'wiazka': wiazka,
    }
    return render(request, 'bledy/form_karta.html', context)


@login_required
def detal_karta(request, id):
    wpis = get_object_or_404(Karta, pk=id)
    wszystkie_wpisy = Bledy.objects.filter(nr_karty=wpis.id)
    if request.user.is_authenticated:
        zglaszajacy_wpisy = get_author(request.user)
        lista_userow = get_user_model()
        autor_wpisu = get_object_or_404(lista_userow, username__exact=zglaszajacy_wpisy)
        lista_autors = Autor.objects.filter(user_id=autor_wpisu.id).values_list('id', flat=True)
        id_autor = lista_autors[0]

        zalogowany_user = request.user
        zalogowany_user_id = request.user.id

    context = {
        'wpis': wpis,
        'wszystkie_wpisy': wszystkie_wpisy,
        'zalogowany_user_id': zalogowany_user_id,
        'zalogowany_user': zalogowany_user,
        'id_autor': id_autor,
    }

    return render(request, 'bledy/karta.html', context)


@login_required
def edytuj_blad_wpis(request, id):
    wpis = get_object_or_404(Bledy, pk=id)
    karta_wpis = Karta.objects.filter(pk=wpis.nr_karty)

    wpisy = BledyForm(request.POST or None, request.FILES or None, instance=wpis)
    wiazka = Wiazka.objects.filter(aktywny=True).order_by('nazwa_wiazki')
    grupa = GrupaRobocza.objects.filter(aktywna=True).order_by('nr_grupy')
    budujacy = Pracownik.objects.filter(zatrudniony=True).order_by('nr_pracownika')
    rodzajBledu = RodzajeBledu.objects.filter(aktywny=True).order_by('blad')
    moja_Data = datetime.now()
    data_dodania = moja_Data.strftime("%Y-%m-%d")

    print('wiązka - numer karty: ', wpis.id)
    print('wiązka - numer karty: ', wpis.nr_karty)
    for kartaWpis in karta_wpis:
        print('karta - numer karty: ', kartaWpis)
        print('karta - numer karty: ', kartaWpis.id)
        print('karta - numer karty: ', kartaWpis.nr_zlecenia)
        print('karta - numer karty: ', kartaWpis.nr_wiazki)

    if wpisy.is_valid():
        wpisy.save()
        return redirect(ostatnie_wpisy)
    else:
        print('Nie jest VALID!')
        print('Error: ', wpisy.errors)

    context = {
        'wpisy': wpisy,
        'wpis': wpis,
        'wiazka': wiazka,
        'grupa': grupa,
        'budujacy': budujacy,
        'rodzajBledu': rodzajBledu,
        'data_dodania': data_dodania
    }
    #print('rodzajReklamacji:', wpisy.instance.rodzaj_reklamacji)

    return render(request, 'bledy/form_bledy_wpisy_ed.html', context)


@login_required
def usun_blad_wpis(request, id):
    wpis = get_object_or_404(Bledy, pk=id)
    form_blad_wpis = SkasowacBledy(request.POST or None, request.FILES or None, instance=wpis)

    if form_blad_wpis.is_valid():
        kasuj = form_blad_wpis.save(commit=False)
        kasuj.skasowany = 1
        kasuj.save()
        return redirect(ostatnie_wpisy)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz.html', context)


@login_required
def zakoncz_blad_wpis(request, id):
    wpis = get_object_or_404(Bledy, pk=id)
    form_blad_wpis = SkasowacBledy(request.POST or None, request.FILES or None, instance=wpis)

    if form_blad_wpis.is_valid():
        kasuj = form_blad_wpis.save(commit=False)
        kasuj.zakonczony = 1
        kasuj.save()
        return redirect(ostatnie_wpisy)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz_zakoncz.html', context)


@login_required
def przywroc_blad_wpis(request, id):
    wpis = get_object_or_404(Bledy, pk=id)
    form_blad_wpis = SkasowacBledy(request.POST or None, request.FILES or None, instance=wpis)

    if form_blad_wpis.is_valid():
        kasuj = form_blad_wpis.save(commit=False)
        kasuj.skasowany = 0
        kasuj.save()
        return redirect(ostatnie_wpisy)

    context = {
        'wpis': wpis
    }
    return render(request, 'bledy/potwierdz.html', context)


def is_valid_queryparam(param):
    return param != '' and param is not None


@login_required
def filtrowanie_bledy_n(request):
    qs = Bledy.objects.filter(skasowany=False)
    nr_budujacego_contains_query = request.GET.get('nr_budujacego_contains')
    blad_contains_query = request.GET.get('blad_contains')
    nr_grupy_roboczej_contains_query = request.GET.get('nr_grupy_roboczej_contains')
    grupabledow_contains_query = request.GET.get('grupa_bledow_contains')
    data_od = request.GET.get('data_od')
    data_do = request.GET.get('data_do')
    eksport = request.GET.get('eksport')

    if is_valid_queryparam(nr_budujacego_contains_query):
        qs = qs.filter(nr_budujacego__nr_pracownika__exact=nr_budujacego_contains_query)
    if is_valid_queryparam(nr_grupy_roboczej_contains_query):
        qs = qs.filter(nr_grupy_roboczej__nr_grupy__icontains=nr_grupy_roboczej_contains_query)
    if is_valid_queryparam(grupabledow_contains_query):
        qs = qs.select_related('blad').filter(blad__grupa_bledow__nazwa__icontains=grupabledow_contains_query)
    if is_valid_queryparam(blad_contains_query):
        qs = qs.filter(blad__blad__icontains=blad_contains_query)
    if is_valid_queryparam(data_od):
        qs = qs.filter(data_dodania__gte=data_od + ' 00:00:00')
    if is_valid_queryparam(data_do):
        qs = qs.filter(data_dodania__lt=data_do + ' 23:59:59')

    lista = []
    date_start = datetime.strptime('2023-05-12 00:00:00', '%Y-%m-%d %H:%M:%S')

    if eksport == 'on':
        for obj in qs:
            if obj.data_dodania >= date_start:
                qs_karty = Karta.objects.filter(id=obj.nr_karty)
                for karta2 in qs_karty:
                    budujacy = "{} {}".format(obj.nr_budujacego.nazwisko, obj.nr_budujacego.imie)
                    if karta2.zolta == True:
                        zolta = 'Tak'
                    else:
                        zolta = 'Nie'
                    #print('nr_karty: {}/{}/{}'.format(karta2.nr_karty, karta2.data_karty_miesiac, karta2.data_karty_rok))
                    #print('nr wiązki: {} || nr zlecenia: {} || wadliwych: {}'.format(karta2.nr_wiazki,karta2.nr_zlecenia,karta2.ilosc_wadliwych))
                    #print('nr_budujacego: {} || blad: {}'.format(obj.nr_budujacego, obj.blad, obj.opis))
                    lista.append((
                        '{}/{}/{}'.format(karta2.id, karta2.data_karty_miesiac, karta2.data_karty_rok),
                        karta2.nr_wiazki,
                        karta2.nr_zlecenia,
                        karta2.ilosc_wadliwych,
                        obj.nr_budujacego,
                        budujacy,
                        obj.nr_grupy_roboczej,
                        obj.blad,
                        obj.opis,
                        zolta,
                        obj.blad.grupa_bledow,
                        karta2.nr_wiazki.nazwa_klienta,
                        karta2.autor_wpisu,
                        karta2.data_dodania)
                    )
                print('- ' * 40)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="eksport_bledy.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'Nr karty',
                'Nr wiazki',
                'Nr zlecenia',
                'Ilość wadliwych',
                'Nr oosoby budującej',
                'Budujacy',
                'Nr grupy roboczej',
                'Blad',
                'opis',
                'żółta',
                'GrupaBledow',
                'Nazwa klienta',
                'autor_wpisu',
                'data_dodania'
            ]
        )

        for wiersz in lista:
            writer.writerow(
                [
                    wiersz[0],
                    wiersz[1],
                    wiersz[2],
                    wiersz[3],
                    wiersz[4],
                    wiersz[5],
                    wiersz[6],
                    wiersz[7],
                    wiersz[8],
                    wiersz[9],
                    wiersz[10],
                    wiersz[11],
                    wiersz[12],
                    wiersz[13]
                ]
            )
        return response



    context = {
        'queryset': qs,
    }
    return render(request, 'bledy/eksport_bledy.html', context)

@login_required
def filtrowanie_karty_n(request):
    qs = Karta.objects.filter(wycofana=False)
    nr_wiazki_contains_query = request.GET.get('nr_wiazki_contains')
    nr_zlecenia_contains_query = request.GET.get('nr_zlecenia_contains')
    klient_contains_query = request.GET.get('klient_contains')
    data_od = request.GET.get('data_od')
    data_do = request.GET.get('data_do')
    eksport = request.GET.get('eksport')

    if is_valid_queryparam(nr_wiazki_contains_query):
        qs = qs.filter(nr_wiazki__nazwa_wiazki__icontains=nr_wiazki_contains_query)
    if is_valid_queryparam(nr_zlecenia_contains_query):
        qs = qs.filter(nr_zlecenia__icontains=nr_zlecenia_contains_query)
    if is_valid_queryparam(klient_contains_query):
        qs = qs.select_related('nr_wiazki').filter(nr_wiazki__nazwa_klienta__nazwa_klienta__icontains=klient_contains_query)
    if is_valid_queryparam(data_od):
        qs = qs.filter(data_dodania__gte=data_od + ' 00:00:00')
    if is_valid_queryparam(data_do):
        qs = qs.filter(data_dodania__lt=data_do + ' 23:59:59')

    lista = []

    date_start = datetime.strptime('2023-06-12 00:00:00', '%Y-%m-%d %H:%M:%S')

    if eksport == 'on':
        for obj in qs:
            if obj.data_dodania >= date_start:
                qs_bledy = Bledy.objects.filter(skasowany=False).filter(nr_karty = obj.id)
                if obj.zolta == True:
                    zolta = 'Tak'
                else:
                    zolta = 'Nie'
                if len(qs_bledy) > 0:
                    for blad2 in qs_bledy:
                        budujacy = "{} {}".format(blad2.nr_budujacego.nazwisko, blad2.nr_budujacego.imie)
                        #print('nr_karty: {}/{}/{}'.format(obj.nr_karty,obj.data_karty_miesiac,obj.data_karty_rok))
                        #print('nr wiązki: {} || nr zlecenia: {} || wadliwych: {}'.format(obj.nr_wiazki,obj.nr_zlecenia,obj.ilosc_wadliwych))
                        #print('nr_budujacego: {} || nr_grupy_roboczej: {} || blad: {}'.format(budujacy,blad2.nr_grupy_roboczej,blad2.blad))
                        #print('klient: {}'.format(obj.nr_wiazki.nazwa_klienta))
                        lista.append((
                            '{}/{}/{}'.format(obj.id,obj.data_karty_miesiac,obj.data_karty_rok),
                            obj.nr_wiazki,
                            obj.nr_zlecenia,
                            obj.ilosc_wadliwych,
                            blad2.nr_budujacego,
                            budujacy,
                            blad2.nr_grupy_roboczej,
                            blad2.blad,
                            blad2.opis,
                            zolta,
                            blad2.blad.grupa_bledow,
                            obj.nr_wiazki.nazwa_klienta,
                            obj.autor_wpisu,
                            obj.data_dodania)
                        )
                else:
                    #print('-->> nr_karty: {}/{}/{}'.format(obj.nr_karty, obj.data_karty_miesiac, obj.data_karty_rok))
                    #print('-->> nr wiązki: {} || nr zlecenia: {} || wadliwych: {}'.format(obj.nr_wiazki, obj.nr_zlecenia, obj.ilosc_wadliwych))
                    #print('-->> nr_budujacego: brak || nr_grupy_roboczej: brak || blad: 0')
                    lista.append((
                        '{}/{}/{}'.format(obj.nr_karty, obj.data_karty_miesiac, obj.data_karty_rok),
                        obj.nr_wiazki,
                        obj.nr_zlecenia,
                        obj.ilosc_wadliwych,
                        'brak',
                        'brak',
                        'brak',
                        'brak',
                        'brak',
                        'brak',
                        'brak',
                        obj.nr_wiazki.nazwa_klienta,
                        obj.autor_wpisu,
                        obj.data_dodania)
                    )
                print('- '*40)


        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="eksport_karty.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'Nr karty',
                'Nr wiazki',
                'Nr zlecenia',
                'Ilość wadliwych',
                'Nr oosoby budującej',
                'Budujacy',
                'Nr grupy roboczej',
                'Blad',
                'opis',
                'Informacyjna',
                'GrupaBledow',
                'Nazwa klienta',
                'autor_wpisu',
                'data_dodania'
            ]
        )

        for wiersz in lista:
            writer.writerow(
                [
                    wiersz[0],
                    wiersz[1],
                    wiersz[2],
                    wiersz[3],
                    wiersz[4],
                    wiersz[5],
                    wiersz[6],
                    wiersz[7],
                    wiersz[8],
                    wiersz[9],
                    wiersz[10],
                    wiersz[11],
                    wiersz[12],
                    wiersz[13]
                ]
            )
        return response



    context = {
        'queryset': qs,
    }
    return render(request, 'bledy/eksport_karty.html', context)


@login_required
def filtrowanie(request):
    qs = Bledy.objects.filter(skasowany=False)
    #qs = Bledy.objects.all()
    #dzial = Dzial.objects.filter(aktywny=True).order_by('dzial')
    nr_wiazki_contains_query = request.GET.get('nr_wiazki_contains')
    nr_grupy_roboczej_contains_query = request.GET.get('nr_grupy_roboczej_contains')
    nr_zlecenia_contains_query = request.GET.get('nr_zlecenia_contains')
    nr_budujacego_contains_query = request.GET.get('nr_budujacego_contains')
    blad_contains_query = request.GET.get('blad_contains')
    grupabledow_contains_query = request.GET.get('grupa_bledow_contains')
    klient_contains_query = request.GET.get('klient_contains')
    data_od = request.GET.get('data_od')
    data_do = request.GET.get('data_do')
    eksport = request.GET.get('eksport')

    print('data_od', data_od)
    print('data_do', data_do)

    if is_valid_queryparam(nr_wiazki_contains_query):
        qs = qs.filter(nr_wiazki__nazwa_wiazki__icontains=nr_wiazki_contains_query)
    if is_valid_queryparam(nr_grupy_roboczej_contains_query):
        qs = qs.filter(nr_grupy_roboczej__nr_grupy__icontains=nr_grupy_roboczej_contains_query)
    if is_valid_queryparam(nr_zlecenia_contains_query):
        qs = qs.filter(nr_zlecenia__icontains=nr_zlecenia_contains_query)
    if is_valid_queryparam(nr_budujacego_contains_query):
        qs = qs.filter(nr_budujacego__nr_pracownika__exact=nr_budujacego_contains_query)
    if is_valid_queryparam(blad_contains_query):
        qs = qs.filter(blad__blad__icontains=blad_contains_query)
    if is_valid_queryparam(grupabledow_contains_query):
        qs = qs.select_related('blad').filter(blad__grupa_bledow__nazwa__icontains=grupabledow_contains_query)
    if is_valid_queryparam(klient_contains_query):
        qs = qs.select_related('nr_wiazki').filter(nr_wiazki__nazwa_klienta__nazwa_klienta__icontains=klient_contains_query)
    if is_valid_queryparam(data_od):
        qs = qs.filter(data_dodania__gte=data_od + ' 00:00:00')
    if is_valid_queryparam(data_do):
        qs = qs.filter(data_dodania__lt=data_do + ' 23:59:59')

    date_end = datetime.strptime('2023-05-28 00:00:00', '%Y-%m-%d %H:%M:%S')

    if eksport == 'on':

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="eksport_stary.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        #mojaData = datetime.now()
        #formatedDate = mojaData.strftime("%Y-%m-%d")

        #print(formatedDate)

        writer = csv.writer(response, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'nr_wiazki',
                'Klient',
                'nr_grupy_roboczej',
                'nr_zlecenia',
                'nr_budujacego',
                'budujacy',
                'ilosc_skontrolowanych',
                'ilosc_bledow',
                'blad',
                'GrupaBledow',
                'opis',
                'autor_wpisu',
                'data_dodania'
            ]
        )

        for obj in qs:
            if obj.data_dodania < date_end:
                budujacy = "{} {}".format(obj.nr_budujacego.nazwisko, obj.nr_budujacego.imie)
                writer.writerow(
                    [
                        obj.nr_wiazki,
                        obj.nr_wiazki.nazwa_klienta,
                        obj.nr_grupy_roboczej,
                        obj.nr_zlecenia,
                        obj.nr_budujacego,
                        budujacy,
                        obj.ilosc_skontrolowanych,
                        obj.ilosc_bledow,
                        obj.blad,
                        obj.blad.grupa_bledow,
                        obj.opis,
                        obj.autor_wpisu,
                        obj.data_dodania
                    ]
                )
        return response

    context = {
        'queryset': qs,
    }
    return render(request, 'bledy/eksport2.html', context)



def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info( request, f"Witaj {username}! Właśnie się zalogowałeś.")
                return redirect("/")
            else:
                messages.error(request, f"Błędny login lub hasło")
        else:
            messages.error(request, f"- Błędny login lub hasło -")
    form = AuthenticationForm()

    context = {
        "form": form
    }
    return render(request, "bledy/login.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "Właśnie się wylogowałeś")
    return redirect(ostatnie_wpisy)


# -- TEST CSV ------------------------------------------------

def upload_file_view(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated = False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                    row = "".join(row)
                    row = row.replace(";", " ")
                    row = row.split()
                    # - PRACOWNICY ------------------------------
                    #r_dzial = Dzial.objects.get(id=row[3])

                    #Pracownik.objects.create(
                    #    nr_pracownika = int(row[0]),
                    #    imie = row[2],
                    #    nazwisko = row[1],
                    #    dzial = r_dzial,
                    #    zatrudniony = 1,
                    #)
                    #print(r_dzial)
                    # - KONIEC PRACOWNICY ------------------------------
                    # =================================================
                    # - KLIENCI ------------------------------
                    #r_dzial = Dzial.objects.get(id=row[3])

                    #Klient.objects.create(
                    #    nazwa_klienta = row[1],
                    #    aktywny = 1,
                    #)
                    #print(row[1])
                    # - KONIEC KLIENCI ------------------------------
                    # =================================================
                    # - WIAZKI ------------------------------
                    #r_klient = Klient.objects.get(id=row[1])

                    #Wiazka.objects.create(
                    #    nazwa_wiazki = row[0],
                    #    nazwa_klienta = r_klient,
                    #    aktywny = 1,
                    #)
                    #print(row[0], row[1], " | ", r_klient)
                    #print(row[0]," || ", row[1]," || ", row[3])
                    # - KONIEC WIAZKI ------------------------------
                    # =================================================
            obj.activated = True
            obj.save()
    context = {
        "form": form
    }
    return render(request, 'bledy/form_upload.html', context)


@login_required
def detal_karta_test(request):
    wszystkie_karty = Karta.objects.filter(wycofana=False).order_by('-id')

    for karty in wszystkie_karty:
        print('{} | {} | {} | {} |*|'.format(karty.nr_karty, karty.data_dodania, karty.nr_wiazki, karty.nr_zlecenia))

    #for karty in wszystkie_karty:
    #    wszystkie_bledy = Bledy.objects.filter(skasowany=False).filter(nr_karty=karty.id)
    #    for bledy in wszystkie_bledy:
    #        print('{} | {} | {} | {} |*| {} | {}'.format(karty.nr_karty, karty.data_dodania, karty.nr_wiazki, karty.nr_zlecenia, bledy.nr_grupy_roboczej, bledy.nr_budujacego))

    context = {
        'wszystkie_karty': wszystkie_karty
    }

    return render(request, 'bledy/karty_test.html', context)