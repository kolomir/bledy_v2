from django.contrib import admin
from .models import RodzajeBledu, GrupaRobocza, Klient, Wiazka, Dzial, Pracownik, Autor, Bledy, RodzajReklamacji, Csv, GrupaBledow, Lider_dzial, Karta


@admin.register(Lider_dzial)
class Lider_dzial(admin.ModelAdmin):
    list_display = ('user', 'dzial',)
    list_filter = ('user', 'dzial',)
    search_fields = ('user', 'dzial',)


@admin.register(RodzajeBledu)
class BladAdmin(admin.ModelAdmin):
    list_display = ('blad', 'grupa_bledow', 'aktywny')
    list_filter = ('grupa_bledow', 'aktywny',)
    search_fields = ('blad', 'aktywny')


@admin.register(Karta)
class KartaAdmin(admin.ModelAdmin):
    list_display = ('nr_karty', 'data_karty_miesiac', 'data_karty_rok', 'data_dodania', 'wycofana', 'zolta', 'wydrukowana')
    list_filter = ('data_karty_miesiac', 'data_karty_rok', 'wycofana', 'zolta', 'wydrukowana')
    search_fields = ('nr_karty', 'data_karty_miesiac', 'data_karty_rok', 'data_dodania', 'wycofana')


@admin.register(GrupaBledow)
class GrupaBledowAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'aktywna')
    list_filter = ('aktywna',)
    search_fields = ('nazwa', 'aktywna')


@admin.register(GrupaRobocza)
class GrupaRoboczaAdmin(admin.ModelAdmin):
    list_display = ('nr_grupy', 'aktywna')
    list_filter = ('aktywna',)
    search_fields = ('nr_grupy', 'aktywna')


@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ('nazwa_klienta', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('nazwa_klienta', 'aktywny')


@admin.register(Wiazka)
class WiazkaAdmin(admin.ModelAdmin):
    list_display = ('nazwa_wiazki', 'nazwa_klienta', 'aktywny')
    list_filter = ('nazwa_klienta', 'aktywny')
    search_fields = ('nazwa_wiazki', 'nazwa_klienta__nazwa_klienta', 'aktywny')


@admin.register(Dzial)
class DzialAdmin(admin.ModelAdmin):
    list_display = ('dzial', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('dzial', 'aktywny')


@admin.register(Pracownik)
class PracownikAdmin(admin.ModelAdmin):
    list_display = ('nr_pracownika', 'imie', 'nazwisko', 'dzial', 'zatrudniony')
    list_filter = ('dzial', 'zatrudniony')
    search_fields = ('nr_pracownika', 'imie', 'nazwisko', 'dzial__dzial', 'zatrudniony')


@admin.register(RodzajReklamacji)
class RodzajReklamacji(admin.ModelAdmin):
    list_display = ('rodzaj', 'aktywny')
    list_filter = ('aktywny',)
    search_fields = ('rodzaj', 'aktywny')


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('user', 'dzial', 'lider', 'kontrol', 'jakosc', 'wzorce')
    list_filter = ('dzial',)


@admin.register(Bledy)
class BledyAdmin(admin.ModelAdmin):
    list_display = (
            'nr_wiazki',
            'nr_grupy_roboczej',
            'nr_zlecenia',
            'nr_kontrolera',
            'nr_budujacego',
            'ilosc_skontrolowanych',
            'ilosc_bledow',
            'blad',
            'autor_wpisu',
            'komputer_user',
            'komputer',
            'data_dodania',
            'skasowany',
            'zakonczony'
    )
    list_filter = (
            'nr_grupy_roboczej',
            'blad',
            'skasowany'
    )
    search_fields = (
            'nr_wiazki__nazwa_wiazki',
            'nr_grupy_roboczej__nr_grupy',
            'nr_zlecenia',
            'nr_kontrolera',
            'nr_budujacego__nr_pracownika',
            'ilosc_skontrolowanych',
            'ilosc_bledow',
            'blad__blad',
            'data_dodania',
            'skasowany',
            'zakonczony'
    )


# -- TEST CSV ------------------------------------------------
admin.site.register(Csv)

