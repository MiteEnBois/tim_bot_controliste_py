def intput(min=-1000000000, max=1000000000, msg="Entrez une valeur"):
    num = 0
    while 1:
        try:
            num = int(input(msg))
        except ValueError:
            print("mauvais input, entrez un nombre svp\n")
            continue
        if(num > max or num < min):
            print("Fait pas le malin, met une valeur adéquate\n")
            continue
        return num
