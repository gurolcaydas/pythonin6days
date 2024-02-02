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
ilkListe = ["1","2","3","2"]
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
ikinciListe=["A","B","C"]
ilkListe.extend(ikinciListe)
ilkListe.pop(1)
print(ilkListe)
for x in ilkListe:
    print(x)


