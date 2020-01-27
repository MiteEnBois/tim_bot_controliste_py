# -*-coding:utf-8 -*
# annee = input("Saississez une année ")
annee = "2000dsfd"
c = True
try:  # On essaye de convertir l'année en entier
    annee = int(annee)
except:
    print("Erreur lors de la conversion de l'année.")
    c = False

if c:

    bi = "bissextile"
    bis = False

    if(annee % 400 == 0 or (annee % 4 == 0 and annee % 100 != 0)):
        print(bi)
    else:
        print("pas "+bi)
