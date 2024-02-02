import random
#This is my first python code
print ("Hello Wrold!")
a,b,c=1,2,3
x=y=z=2
q=float(20.4)
g="text"
h=random.randrange(1,100)
def ilkFunction():
    print("ilk fonksiyon")
def ikinciFunc():
    print("Random100 ",h)
print(type(g))
# if (x>2):
#     print("x>2")
# else:
#     print("x<=2")
ilkFunction() 
ikinciFunc()
if ("ex" in g):
    print("var")
if ("erx" not in g):
    print("yok")

# print(g[1:3])
# print(g[:3])
j="Falan {1} \nfilan {0}"
# print(j.format(b,a).upper())
## string methods çalışılacak.
## https://www.w3schools.com/python/python_strings_methods.asp
ilkListe = ["1",2,3,"2"]
# print (ilkListe[0:2])
# print (ilkListe.count("2"))
# print(type(ilkListe))
if ("3" in ilkListe):
    print("var")
else:
    print("yok")
ilkListe[2]="4"
# print (ilkListe)
ilkListe.insert(1,"0")
ilkListe.append("5")
# print(ilkListe)
ikinciListe=["Adana","Istanbul","Ankara","B","Rize"]
ilkListe.extend(ikinciListe)
ilkListe.pop(1)
print(ilkListe)
# for x in ilkListe:
#     print(x)
# [print(x) for x in ilkListe]
yeniListe = [x for x in ilkListe if isinstance(x, str) and "n" in x]
print(yeniListe)
# yeniListe = [x for x in ilkListe if type(x) is not int]
# print (len(yeniListe))
yeniListe.sort()
print(yeniListe)
thistuple = tuple(("apple", "banana", "cherry", "apple", "cherry"))
print(thistuple)
thisset = {"apple", "banana", "cherry"}
print(thisset)
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)
# for x in thisdict:
#   print(thisdict[x])
# for x, y in thisdict.items():
#   print("key: ",x," value: ", y)
# for x in range(2, 6):
#   print(x)
kup = lambda a,b : a**b
print (kup(2,3))

class teneke:
    def __init__(self,ad,soyad):
        self.ad = ad
        self.soyad = soyad
    def bilgileri(self):
        print(self.ad,self.soyad)
t1 = teneke("adı","soyadı")
t1.bilgileri()
print(t1.ad)


