import math
def name_func():
    print("Hello")
    name = input("Skriv in namn: ")
    return name
    
def radie_func(radie):
    try:
        radie = int(input("Skriv in radie (cm): "))
    except:
        print("Något gick fel, försök igen!")
        radie_func(0)
    return radie

def cirkel_calc(radie):
    pi=math.pi
    area = pi * (radie **2)
    area = round(area, 2)
    return area

def hojd_func(hojd):
    try:
        hojd = int(input("Skriv in höjd för kon/cylinder (cm): "))
    except:
        print("Något gick fel, försök igen!")
        hojd_func(0)
    return hojd

def volym_kon_func(area, hojd):
    volym_kon = (area * hojd)/3
    volym_kon = round(volym_kon, 2)
    return volym_kon

def cylle_func(area, hojd):
    cylle_vol = area * hojd
    cylle_vol = round(cylle_vol, 2) 
    return cylle_vol

name = name_func()
radie = radie_func(0)
area = cirkel_calc(radie)
print(f"{name} cirkels area är {area} kvadratcentimeter")
hojd = hojd_func(0)
volym_kon = volym_kon_func(area, hojd)
volym_cylle = cylle_func(area, hojd)
print(f"{name} kon har volymen {volym_kon} kubikcm")
print(f"{name} cylinder har volymen {volym_cylle} kubikcm")