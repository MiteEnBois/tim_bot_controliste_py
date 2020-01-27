import random
import math
import time
from functions import intput


min = 0
max = 49
money = 500
print("Bienvenue au ZCasino\n")
while 1:

    print("Vous avez", money, "$\n")

    bet = intput(0, money, "Entrez votre mise : ")
    money -= bet
    print("Vous avez", money, "$ maintenant\n")
    num = intput(min, max, "Sur quelle case voulez vous miser? ")

    print("Rien ne va plus!")
    rmax = random.randrange(3, 5)
    i = 0
    while(i <= rmax):
        time.sleep(1)
        print("La roue tourne...")
        i += 1
    tombe = random.randrange(min, max)
    print("Et tombe sur le ", tombe, "!!!")
    if tombe == num:
        print("Vous etes le grand gangant! Vous gagnez", bet*3, "$!!!!!!!!!!!!")
        money += bet*3
    elif tombe % 2 == num % 2:
        print("Vous etes pas le grand gangant, mais vous etes tombé sur la meme couleur. Vous gagnez", math.ceil(bet/2), "$")
        money -= math.ceil(bet/2)
    else:
        print("Pas de chance, vous n'avez rien eu. Quel dommage")
    if money <= 0:
        print("Désolé, mais on ne sert pas les pauvres")
        break
    rep = input("Voulez vous rejouer? o/n\n")
    if rep == "o":
        continue
    else:
        break
print("Votre argent final :", money, "$")
