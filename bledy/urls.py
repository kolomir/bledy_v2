from django.urls import path, include
from .views import ostatnie_wpisy, nowy_klient, edytuj_klient, wpisyKlient, usun_klient, przywroc_klient, \
                nowa_grupa, edytuj_grupa, wpisyGrupaRobocza, usun_grupa, przywroc_grupa, \
                nowy_dzial, edytuj_dzial, wpisyDzialy, usun_dzial, przywroc_dzial, \
                nowy_blad, edytuj_blad, wpisyBlad, usun_blad, przywroc_blad, \
                nowa_wiazka, edytuj_wiazka, wpisyWiazka, usun_wiazke, przywroc_wiazke, \
                nowy_pracownik, edytuj_pracownik, wpisyPracownik, usun_pracownik, przywroc_pracownik, \
                nowy_blad_wpis, edytuj_blad_wpis, usun_blad_wpis, przywroc_blad_wpis, filtrowanie, \
                login_request, logout_request, upload_file_view, nowa_grupa_bledow, edytuj_grupa_bledow, \
                usun_grupa_bledow, przywroc_grupa_bledow, wpisyGrupaBledow, wpisy_lider_dzial, przypisz_lider_dzial, \
                zakoncz_blad_wpis, nowaKarta, wpisyKarta, wszystkie_wpisy, detal_karta


urlpatterns = [
    path('', ostatnie_wpisy, name='ostatnie_wpisy'),
    #= Nowy ===============================================
    path('klienciForm/', nowy_klient, name='klienciForm'),
    path('grupyForm/', nowa_grupa, name='grupyForm'),
    path('dzialyForm/', nowy_dzial, name='dzialyForm'),
    path('bledyForm/', nowy_blad, name='bledyForm'),
    path('wiazkaForm/', nowa_wiazka, name='wiazkaForm'),
    path('pracownikForm/', nowy_pracownik, name='pracownikForm'),
    path('bledy_wpisForm/', nowy_blad_wpis, name='bledy_wpisForm'),
    path('bledy_wpisForm/', nowy_blad_wpis, name='bledy_wpisForm'),
    path('grupy_bledowForm/', nowa_grupa_bledow, name='grupy_bledowForm'),
    path('przypisz_lider_dzial/', przypisz_lider_dzial, name='przypisz_lider_dzial'),
    path('form_karta/', nowaKarta, name='nowaKarta'),

    #= Edycja =============================================
    path('klienciFormedytuj/<int:id>/', edytuj_klient, name='klienciFormedytuj'),
    path('grupyFormedytuj/<int:id>/', edytuj_grupa, name='grupyFormedytuj'),
    path('grupy_bledowFormedytuj/<int:id>/', edytuj_grupa_bledow, name='grupy_bledowFormedytuj'),
    path('dzialyFormedytuj/<int:id>/', edytuj_dzial, name='dzialyFormedytuj'),
    path('bledyFormedytuj/<int:id>/', edytuj_blad, name='bledyFormedytuj'),
    path('wiazkaFormedytuj/<int:id>/', edytuj_wiazka, name='wiazkaFormedytuj'),
    path('pracownikFormedytuj/<int:id>/', edytuj_pracownik, name='pracownikFormedytuj'),
    path('bledy_edytujForm/<int:id>/', edytuj_blad_wpis, name='bledy_edytujForm'),

    #= Zestawienie ========================================
    path('klienci/', wpisyKlient, name='klienci'),
    path('grupyrobocze/', wpisyGrupaRobocza, name='grupyrobocze'),
    path('grupybledow/', wpisyGrupaBledow, name='grupybledow'),
    path('dzialy/', wpisyDzialy, name='dzialy'),
    path('bledy/', wpisyBlad, name='bledy'),
    path('wiazka/', wpisyWiazka, name='wiazka'),
    path('pracownik/', wpisyPracownik, name='pracownik'),
    #path('', wszystkie_wpisy, name='wszystkie_wpisy'),
    path('lider_dzial/', wpisy_lider_dzial, name='lider_dzial'),
    path('wszystkie_karty/', wpisyKarta, name='wpisyKarta'),
    path('wszystkie_wpisy/', wszystkie_wpisy, name='wszystkie_wpisy'),
    path('detal_karta/<int:id>/', detal_karta, name='detal_karta'),
    path('detal_karta/<int:id>/', detal_karta, name='detal_karta'),

    #= Kasowanie ==========================================
    path('usun_klient/<int:id>/', usun_klient, name='usun_klient'),
    path('usun_grupa/<int:id>/', usun_grupa, name='usun_grupa'),
    path('usun_grupa_bledow/<int:id>/', usun_grupa_bledow, name='usun_grupa_bledow'),
    path('usun_dzial/<int:id>/', usun_dzial, name='usun_dzial'),
    path('usun_blad/<int:id>/', usun_blad, name='usun_blad'),
    path('usun_wiazke/<int:id>/', usun_wiazke, name='usun_wiazke'),
    path('usun_pracownik/<int:id>/', usun_pracownik, name='usun_pracownik'),
    path('usun_bledy/<int:id>/', usun_blad_wpis, name='usun_bledy'),
    path('zakoncz_bledy/<int:id>/', zakoncz_blad_wpis, name='zakoncz_bledy'),

    #= Przywracanie =======================================
    path('przywroc_klient/<int:id>/', przywroc_klient, name='przywroc_klient'),
    path('przywroc_grupa/<int:id>/', przywroc_grupa, name='przywroc_grupa'),
    path('przywroc_grupa_bledow/<int:id>/', przywroc_grupa_bledow, name='przywroc_grupa_bledow'),
    path('przywroc_dzial/<int:id>/', przywroc_dzial, name='przywroc_dzial'),
    path('przywroc_blad/<int:id>/', przywroc_blad, name='przywroc_blad'),
    path('przywroc_wiazke/<int:id>/', przywroc_wiazke, name='przywroc_wiazke'),
    path('przywroc_pracownik/<int:id>/', przywroc_pracownik, name='przywroc_pracownik'),
    path('przywroc_bledy/<int:id>/', przywroc_blad_wpis, name='przywroc_bledy'),

    #= Pozostałe ==========================================
    path('eksport/', filtrowanie, name='filtrowanie'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('upload/', upload_file_view, name='upload'),

    #=TEST=================================================
]