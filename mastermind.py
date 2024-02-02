# mastermind.py
# Python 6 days challenge day #2
import os
import datetime
import random

sayiKumesi = "1234567890QWERTY"
kacKarakter = len(sayiKumesi)
bulmacaHarfSayisi = 6
def temizle():
    # For Windows
    if (os.name == 'nt'):
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')   
def dorkBasamakli(numara):
    if len(numara) != bulmacaHarfSayisi:
        return False
    return True
def farkliHarfler(numara):
    for x in numara:
        if (numara.count(x)>1):
            return False
    return True
def sifirBesArasi(numara):
    for x in numara:
        if (x not in sayiKumesi):
            return False
    return True
def bulmaca(): 
    #sayiKumesi="012345"
    gizli = ""
    while (len(gizli) < bulmacaHarfSayisi):
        siradaki=random.randrange(kacKarakter)
        if (sayiKumesi[siradaki] not in gizli):
            gizli = sayiKumesi[siradaki] + gizli 
    return gizli
def kaciVarYeriYanlis(numara):
    buVar = 0
    for x in numara:
        if (x in bulBeni):
            buVar += 1
    return buVar

def kaciVarYeriDogru(numara):
    buVar = 0
    y=0
    for x in numara:
        if (x == bulBeni[y]):
            buVar += 1
        y += 1
    return buVar

def ekraniYazdir():
    for (x,y) in zip(tahminler, sonuclar):
        print(x,y)
print("--------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------")
print (datetime.datetime.now().strftime("%d of %B"))
oyuncu = input("\nİsminiz: ")
mesaj= " Oyunumuza hoşgeldiniz, "+oyuncu+" "
uzunluk=int((80-len(mesaj))/2)
ondeki="-"*uzunluk 
arkadaki="-"*(uzunluk + len(mesaj) % 2)
tahminler = list(())
sonuclar = list(())
degil4Basamak = 0
degilRakamlarFarkli = 0
degilSifirBes = 0
bulBeni=bulmaca()
tahminSayisi = 0
temizle()
print("--------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------")
print("------------------------------- MasterMind Game --------------------------------")
print("--------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------")
print(ondeki+ mesaj +arkadaki)
print("--------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------")
print("Senin için {} basamaklı bir şifre tuttuk, tahmin edebilir misin?".format(bulmacaHarfSayisi))
print("Acemi Python programcısının eksikleri yüzünden bu {} basamak renklerden değil rakamlardan oluşuyor.".format(bulmacaHarfSayisi))
print("Master Mind oyunun gereği olarak sadece {} çeşit renk yani bu örnekte rakam kullandık".format(len(sayiKumesi)))
print("Yani "+sayiKumesi+" rakamlarıdan oluşan, birbirinin aynı rakamları içermeyen, {} basamaklı bir sifre olacak".format(bulmacaHarfSayisi))
while(True):
    tahmin = input("\nTahmininizi giriniz:")
    if dorkBasamakli(tahmin):
        if farkliHarfler(tahmin):
            if sifirBesArasi(tahmin):
                tahminSayisi += 1
                yeriDogrular=kaciVarYeriDogru(tahmin)
                olanlar=kaciVarYeriYanlis(tahmin) - yeriDogrular
                sonuclar.append("-"+format(olanlar)+" +"+format(yeriDogrular))
                tahminler.append(tahmin)
                ekraniYazdir()
                if yeriDogrular == bulmacaHarfSayisi:
                    print("--------------------------------------------------------------------------------")
                    print("--------------------------------------------------------------------------------")
                    print("Tebrikler sevgili "+oyuncu+", bulmacayı {}. tahminde buldunuz".format(tahminSayisi))
                    print("--------------------------------------------------------------------------------")
                    print("--------------------------------------------------------------------------------")
                    print("Ama bir dakika?!")
                    toplamHataliGiris = degil4Basamak+degilRakamlarFarkli+degilSifirBes
                    if (toplamHataliGiris == 0):
                        print("Sen hiç hatalı giriş yapmamışsın? Bravo kuralcı kişi.")
                    else:
                        if(toplamHataliGiris < 5):
                            print("Az miktarda hatalı girişi her hoca olumlulukla kabul eder.")
                        else:
                            print("Biraz abartılı hatalı giriş olmuş.")
                            if (toplamHataliGiris > 10):
                                print("Bacım sen rastgele basmışsın tuşlara, oynamayacaksan oynamıyorum de, ktrl-C basıp kaçsaydın. Hadi kardeşim CPU'yu oyalama!")
                            else:
                                print("Gereksiz taramalardan kaçınalım!")
                    print("--------------------------------------------------------------------------------")
                    print("----------------------------------------------------------------------------end-")
                    break

            else:
                degilSifirBes += 1
                print("Lütfen "+sayiKumesi+" rakamları den olusan {} basamakli bir sayi giriniz.".format(bulmacaHarfSayisi))
        else:
            degilRakamlarFarkli += 1
            print("Amaaaa lütfen rakamlar birbirinden farklı olsun.")
    else:
        degil4Basamak += 1
        print("Lütfen {} basamakli bir sayi giriniz".format(bulmacaHarfSayisi))
        if degil4Basamak>5:
            print("Bu iş can sıkmaya başladı, {} basamak nedir bilir misin?".format(bulmacaHarfSayisi))



