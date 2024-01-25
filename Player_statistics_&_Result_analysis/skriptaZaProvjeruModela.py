import csv
from collections import defaultdict
import sys

#naci pobjednika za svaki mec
#provjeriti nalaze li se oba igraca u statistickom datasetu(popis igraca je u tablici broj_meceva_igraci_bitno)
#koliko meceva se igralo - 3 ili 5(ako ude u 3. set onda bitno provjeriti)
CSV_COLUMNS = ['SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result', 'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']
CSV_COLUMNS_0 = ['No', 'SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result', 'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']
CSV_IMENA = ['SportEventID', 'Igrac1', 'Igrac2', 'Pobjednik', 'na_koliko_setova_se_igra_mec' ]

#zapisi sve igrace koji su mi bitni u dict
def procitajIgrace(path):
    igraci = defaultdict(dict)
    with open(path, encoding = 'ISO-8859-1') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = ',')
        i=0
        for row in csv_reader:
            igraci[row["ImeIgraca"]] = row["ImeIgraca"]
            i = i+1
    return igraci

#procitaj datoteku i zapisi sve meceve u dict mecevi
#gledam samo meceve gdje su oba igraca u dict-u igraci
def procitajDatoteku(path, counter, igraci):
    mecevi = defaultdict(dict)

    with open(path, encoding = 'ISO-8859-1') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = ',')
        for row in csv_reader:
            id = row["SportEventID"]
            #for i in 
            home = row['Home']
            away = row['Away']
            #print(home)
            #print(away)
            if(home in igraci and away in igraci):
                mecevi[id][row["When"]] = row
                #print(row)
            #elif(home not in igraci):
                #print(home)
            #elif(away not in igraci):
                #print(away)
        return mecevi



def racunajPobjednika(sviMecevi):
    igraci = defaultdict(dict)
    pobjednik = defaultdict(dict)
    kolikoSetova = defaultdict(dict)
    
    count = 0
    for mec in sviMecevi:
        for id in sviMecevi[mec]:
            sifra = sviMecevi[mec][id]["SportEventID"]
            home = sviMecevi[mec][id]['Home']
            away = sviMecevi[mec][id]["Away"]
            
            
            if ("Z" in sviMecevi[mec][id]["Period"] and sifra not in igraci) : 
                rezultat = sviMecevi[mec][id]["Result"]
                razdvojeno = rezultat.split(" ")
                     
               
                #print(home, away)
                #print(razdvojeno)
                
                duljinaMeca = 0
                if(razdvojeno[0][0] > razdvojeno[0][2] and razdvojeno[1][0] > razdvojeno[1][2] and len(razdvojeno) == 2):
                    pobjednik = home
                    duljinaMeca = 3
                elif(razdvojeno[0][0] < razdvojeno[0][2] and razdvojeno[1][0] < razdvojeno[1][2]and len(razdvojeno) == 2):
                    duljinaMeca = 3
                    pobjednik = away
                elif(razdvojeno[0][0] > razdvojeno[0][2] and razdvojeno[1][0] > razdvojeno[1][2]  and razdvojeno[2][0] > razdvojeno[2][2] and len(razdvojeno) == 3):
                    pobjednik = home
                    duljinaMeca = 5
                elif(razdvojeno[0][0] < razdvojeno[0][2] and razdvojeno[1][0] < razdvojeno[1][2]  and razdvojeno[2][0] < razdvojeno[2][2] and len(razdvojeno) == 3):
                    pobjednik = away
                    duljinaMeca = 5
                elif(len(razdvojeno) == 3):
                    i=0
                    for x in razdvojeno:
                        prviPo = 0
                        drugiPo = 0
                        if(razdvojeno[i][0]>razdvojeno[i][2]):
                            prviPo = prviPo + 1
                        elif(razdvojeno[i][0]<razdvojeno[i][2]):
                            drugiPo = drugiPo + 1
                        i=i+1
                    if(prviPo > drugiPo):
                        pobjednik = home
                    elif(prviPo < drugiPo):
                        pobjednik = away
                    duljinaMeca = 3
                elif(len(razdvojeno) == 4 or len(razdvojeno)==5):
                    i=0
                    for x in razdvojeno:
                        prviPo = 0
                        drugiPo = 0
                        if(razdvojeno[i][0]>razdvojeno[i][2]):
                            prviPo = prviPo + 1
                        elif(razdvojeno[i][0]<razdvojeno[i][2]):
                            drugiPo = drugiPo + 1
                        i=i+1
                    if(prviPo > drugiPo):
                        pobjednik = home
                    elif(prviPo < drugiPo):
                        pobjednik = away
                    duljinaMeca = 5
                elif(duljinaMeca == 0):
                    pobjednik = away
                    duljinaMeca = 3
                    print("Greska")
                    #print(home, away)
                    #print(razdvojeno)
                
                #print(pobjednik)
                #print(duljinaMeca)
                igraci[sifra] = [home, away, pobjednik, duljinaMeca]
                count = count +1
    print(count)
    return igraci

#zapisi u datoteku provjeraModela/pobjednici
def zapisiMeceve(igraci):
    path = "provjeraModela/pobjednici.csv"
    try:
        with open(path, 'w', encoding = 'ISO-8859-1') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_IMENA)
            writer.writeheader()
            writer = csv.writer(csvfile)
            for key, value in igraci.items():
                #print(data)
                #print(BROJ_MECEVA_FINAL[data])
                writer.writerow([key, value[0], value[1], value[2], value[3]])

    except IOError:
        print("I/O Error")

def main():
    counter = 0
    igraci = procitajIgrace("statistike/broj_meceva_igraci_bitno")
    sviMecevi = defaultdict(dict) #u tom dictu su svi mecevi kod kojih se oba igraca nalaze u igraci
    for line in sys.stdin:
        path = line.strip()
        mecevi = procitajDatoteku(path, counter, igraci)
        sviMecevi.update(mecevi)
        #print(len(mecevi))
        #izbaciMeceve(mecevi)
    igraci = racunajPobjednika(sviMecevi)
    zapisiMeceve(igraci)
    #print(len(sviMecevi))
    #print(igraci)
main()
#pokretanje programa: 
# cat .\data5.txt | python .\skriptaZaProvjeruModela.py