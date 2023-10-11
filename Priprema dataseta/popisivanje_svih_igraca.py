import csv
from collections import defaultdict
import sys

sviIgraci = [] #lista u kojoj su svi igraci
IMENA = ['ImeIgraca', 'ASCII']
igraciZapisi = dict()

#procitaj imena svih igraca 
def procitajDatoteku(path):
    igraci = []
    mecevi = defaultdict(dict)
    co = 0

    with open(path, encoding = 'ISO-8859-1') as csv_file:
        #print(path)
        csv_reader = csv.DictReader(csv_file, delimiter = ',')
        for row in csv_reader:
            igracHome = row["Home"]
            igracAway = row["Away"]
            if(igracHome not in igraci):
                igraci.append(igracHome)
            if(igracAway not in igraci):
                igraci.append(igracAway)
    return igraci


#provjera jesu li svi znakovi ascii
#True - svi znakovi su ASCII
#False - nisu svi znakovi ASCII
def provjeriAscii(sviIgraciNovo):
    igraciZapisi = defaultdict(dict)
    for i in sviIgraciNovo:
        if(len(i) != len(i.encode()) or "_" in i):
            igraciZapisi[i] = False
        elif(len(i) == len(i.encode())):
            igraciZapisi[i] = True
        
    return igraciZapisi

#zapisi sve igrace u novu datoteku
def zapisiIgrace(igraciZapisi):
    path = "statistike/sviIgraci.csv"
    try:
        with open(path, 'w', encoding = 'ISO-8859-1') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=IMENA)
            writer.writeheader()
            writer = csv.writer(csvfile)
            for key, value in igraciZapisi.items():
                #print(data)
                #print(BROJ_MECEVA_FINAL[data])
                writer.writerow([key, value])

    except IOError:
        print("I/O Error")

def main():
    for line in sys.stdin:
            path = line.strip()
            igraci = procitajDatoteku(path)
            #spremi imena svih igraca u listu
            sviIgraci.extend(igraci)
    #napravi set od liste da maknem duplikate
    maknutiDupli = set(sviIgraci)
    #napravim ponovo listu od seta s izbacenim duplikatima
    sviIgraciNovo = list(maknutiDupli)
    #sortiram abecedno
    sviIgraciNovo.sort(key=str.lower)
    print(len(sviIgraciNovo))
    #print(sviIgraciNovo)
    #zapisem sve igrace u datoteku sviIgraci.csv
    igraciZapisi = provjeriAscii(sviIgraciNovo)
    zapisiIgrace(igraciZapisi)
main()

#pokretanje:
#cat .\data3.txt | python .\sviIgraci.py