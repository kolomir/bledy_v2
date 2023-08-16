from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import socket
import getpass


class Klient(models.Model):
    nazwa_klienta = models.CharField(max_length=40, unique=True)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa_klienta


class GrupaBledow(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    aktywna = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa


class RodzajeBledu(models.Model):
    blad = models.CharField(max_length=100, unique=True)
    grupa_bledow = models.ForeignKey(GrupaBledow, on_delete=models.CASCADE)
    #czy_test = models.BooleanField(default=False)
    #czy_produkcja_cz = models.BooleanField(default=False)
    #czy_produkcja_bs = models.BooleanField(default=False)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.blad


class GrupaRobocza(models.Model):
    nr_grupy = models.CharField(max_length=40, unique=True)
    aktywna = models.BooleanField(default=True)

    def __str__(self):
        return self.nr_grupy


class Wiazka(models.Model):
    nazwa_wiazki = models.CharField(max_length=40, unique=True)
    nazwa_klienta = models.ForeignKey(Klient, on_delete=models.CASCADE)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa_wiazki


class Dzial(models.Model):
    dzial = models.CharField(max_length=20, unique=True)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.dzial


class Pracownik(models.Model):
    nr_pracownika = models.DecimalField(max_digits=4,decimal_places=0, unique=True)
    imie = models.CharField(max_length=20)
    nazwisko = models.CharField(max_length=40)
    dzial = models.ForeignKey(Dzial, on_delete=models.CASCADE)
    zatrudniony = models.BooleanField(default=True)

    def __str__(self):
        return str(self.nr_pracownika)


class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    dzial = models.ForeignKey(Dzial, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class RodzajReklamacji(models.Model):
    rodzaj = models.CharField(max_length=20, unique=True)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.rodzaj


class Karta(models.Model):
    nr_karty = models.DecimalField(max_digits=5, decimal_places=0, default=0)  #
    data_karty_miesiac = models.DecimalField(max_digits=3, decimal_places=0, default=0, blank=True, null=True)
    data_karty_rok = models.DecimalField(max_digits=5, decimal_places=0, default=0, blank=True, null=True)
    data_dodania = models.DateTimeField('data dodania', blank=True, null=True)
    wycofana = models.BooleanField(default=False)
    nr_wiazki = models.ForeignKey(Wiazka, on_delete=models.CASCADE, default=1)  #
    nr_zlecenia = models.CharField(max_length=20)  #
    ilosc_wadliwych = models.DecimalField(max_digits=8, decimal_places=0, default=1)  #
    autor_wpisu = models.ForeignKey(Autor, on_delete=models.CASCADE)
    zolta = models.BooleanField(default=False)
    wydrukowana = models.BooleanField(default=False)

    def __str__(self):
        return "{}/{}/{}".format(self.id.__str__(), self.data_karty_miesiac.__str__(), self.data_karty_rok.__str__())


class Bledy(models.Model):

    hostname = socket.gethostname()
    login_username = getpass.getuser()

    mojaData = datetime.now()
    formatedDate = mojaData.strftime("%Y-%m-%d")

    nr_wiazki = models.ForeignKey(Wiazka, on_delete=models.CASCADE, default=1, blank=True, null=True) # poprawiony
    nr_grupy_roboczej = models.ForeignKey(GrupaRobocza, on_delete=models.CASCADE, default=1) # >>>>>>>>>> Wymagane
    nr_zlecenia = models.CharField(max_length=20, blank=True, null=True) # poprawione
    opis = models.TextField(blank=True, null=True)
    nr_kontrolera = models.DecimalField(max_digits=5, decimal_places=0, default=999, blank=True, null=True) #
    nr_budujacego = models.ForeignKey(Pracownik, on_delete=models.CASCADE, default=1) # >>>>>>>>>> Wymagane
    ilosc_skontrolowanych = models.DecimalField(max_digits=8, decimal_places=0, default=1, blank=True, null=True) # poprawione
    ilosc_bledow = models.DecimalField(max_digits=5, decimal_places=0, default=1) # >>>>>>>>>> Wymagane
    blad = models.ForeignKey(RodzajeBledu, on_delete=models.CASCADE, default=1)# >>>>>>>>>> Wymagane
    rodzaj_reklamacji = models.ForeignKey(RodzajReklamacji, on_delete=models.CASCADE, default=1) #
    autor_wpisu = models.ForeignKey(Autor, on_delete=models.CASCADE)
    komputer_user = models.CharField(max_length=10, default=login_username)
    komputer = models.CharField(max_length=30, default=hostname)
    data_dodania = models.DateTimeField('data dodania', blank=True, null=True)
    skasowany = models.BooleanField(default=False)
    zakonczony = models.BooleanField(default=False)
    #nr_karty = models.ForeignKey(Karta,on_delete=models.CASCADE, default=1) #
    nr_karty = models.DecimalField(max_digits=8, decimal_places=0, default=1) # >>>>>>>>>> Wymagane

    def __str__(self):
        return str(self.nr_wiazki)


class Lider_dzial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lider")
    dzial = models.ForeignKey(GrupaRobocza, on_delete=models.CASCADE)

    def __str__(self):
        return "{}_{}".format(self.user.__str__(), self.dzial.__str__())


# -- TEST CSV ------------------------------------------------

class Csv(models.Model):
    file_name = models.FileField(upload_to = 'csvs')
    uploaded = models.DateTimeField(auto_now_add = True)
    activated = models.BooleanField(default = False)

    def __str__(self):
        return f"File id: {self.id}"

'''
class Model1(models.Model):
    liczba = models.DecimalField(max_digits=5, decimal_places=0, default=0)  #
    opis = models.CharField(max_length=20) #
    def __str__(self):
        return str(self.opis)

class Model2(models.Model):
    numer = models.DecimalField(max_digits=5, decimal_places=0, default=0)  #
    model_dodany = models.ForeignKey(Model1, on_delete=models.CASCADE, related_name="model1")
    data_karty_rok = models.DateTimeField('data karty rok', blank=True, null=True)
    def __str__(self):
        return str(self.numer)
'''