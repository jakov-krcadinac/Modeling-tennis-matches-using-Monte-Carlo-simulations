import csv
from collections import defaultdict
import sys


CSV_COLUMNS_0 = ['No', 'SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']

CSV_COLUMNS = ['SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']

def ASCIIime(ime):
    retVal = True
    for i in ime:
        if ( (i>="a" and i<="z") or (i>="A" and i<="Z") or (i==" ") or (i==".") or (i=="/") or (i=="-")):
            continue
        else:
            retVal=False
    return retVal

def rjecnik_imena_za_zamjenu():

    rjecnikZamjene = {}
    listaZamjene = []

    with open("statistike/sviIgraci.csv", encoding = 'ISO-8859-1') as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
            
            for row in csv_reader:

                if (row["ASCII"] == "False"):   # ako ime igrača ne sadrži samo ASCII znakove treba ga zamijeniti s verzijom imena koje ima samo ASCII znakove
                    #print(row["ImeIgraca"], " mijenjam u ", row["NovoIme"])
                    rjecnikZamjene[row["ImeIgraca"]] = row["NovoIme"]
                    listaZamjene.append(row["ImeIgraca"])
                    #listaZamjene.append(row["NovoIme"])

    print(rjecnikZamjene)
    for i in sorted(rjecnikZamjene.keys()):
        print(i)
    print(len(rjecnikZamjene.keys()))
    print()

    print(sorted(listaZamjene))
    print(len(listaZamjene))
    return listaZamjene

def lista_redova_s_ispravljenim_imenima(path, listaZamjene):
    pravi_path = "filtrirani_final/" + path

    redovi_csv_datoteke = []   # varijabla u koju spremam redove s ispravljenim imenima

    setZamjenjenihIgraca = set()
    setASCIIigraca = set()
    setNeASCIIigraca = set()
    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    
        for row in csv_reader:

            red = []

            #red.append(pravi)
            imaNeASCIIuRedu = False
            for key in row.keys():
                if (key == "Home" or key == "Away"):
                    """
                    if(row[key] in listaZamjene):  #ako se igrac nalazi u popisu igraca cije ime mijenjamo verzijom koja ima samo ASCII znakove
                        setZamjenjenihIgraca.add(row[key])
                        index = listaZamjene.index(row[key])

                        #print(row[key], " koji je u listiZamjene ", listaZamjene[index], "mijenjam sa ", listaZamjene[index+1])

                        red.append(listaZamjene[index+1])    # dodaj u red umjesto originalnog imena izmjenjenu verziju sa samo ASCII znakovima
                    else:
                    """
                    if (ASCIIime(row[key])):
                        setASCIIigraca.add(row[key])
                    else:
                        setNeASCIIigraca.add(row[key])
                        # u suprotnom igrač ima samo ASCII znakove u imenu pa ga ostavljamo normalno u datasetu

                    if(row[key]=="A.Ivanovi" or row[key]=="A.Ivanovi\\x86" or row[key]=="A.Ivanovi\x86"
                         or row[key]=="A.Ivanoviæ" or row[key]=="A.Ivanoviþ" or ("A.Ivanovi" in row[key])):
                        #print("Mijenjam A.Ivanovic")
                        #imaNeASCIIuRedu = True
                        red.append("A.Ivanovic")
                    elif("A.Pavi" in row[key]):
                        red.append("A.Pavic")
                    elif("AndroiÄ T." == row[key] or ("Androi" in row[key] and "T." in row[key])):
                        red.append("Androic T.")
                    elif("Ba_iþ M." == row[key] or "Ba¹iæ M." == row[key]):
                        red.append("Basic M.")
                    elif("Chardy/Ma.¬ili" == row[key] or ("Chardy/Ma." in row[key] and "ili" in row[key])):
                        red.append("Chardy/Ma.Cilic")
                    elif("umhur D." in row[key]):
                        red.append("Dzumhur D.")
                    elif("Giraldo/Lajovi" in row[key]):
                        red.append("Giraldo/Lajovic")
                    elif("Goerges/Marti" in row[key]):
                        red.append("Goerges/Martic")
                    elif("J.Jankovi" in row[key]):
                        red.append("J.Jankovic")
                    elif("Jak" in row[key] and "J." in row[key]):
                        red.append("Jaksic J.")
                    elif("Jakupovi" in row[key]):
                        red.append("Jakupovic D.")
                    elif("Jankovi" in row[key] and "Kruni" in row[key]):
                        red.append("Jankovic/Krunic")
                    elif("Jorovi" in row[key]):
                        red.append("Jorovic I.")
                    elif("Karlovi" in row[key]):
                        red.append("Karlovic I.")
                    elif("Kav" in row[key] and "B." in row[key]):
                        red.append("Kavcic B.")
                    elif("L.Arruab/Klepa" in row[key]):
                        red.append("L.Arruab/Klepac")
                    elif("Klepa" in row[key] and "A." in row[key]):
                        red.append("Klepac A.")
                    elif("Kovini" in row[key] and "D." in row[key]):
                        red.append("Kovinic D.")
                    elif("Kovini" in row[key] and "Vogt" in row[key]):
                        red.append("Kovinic/Vogt")
                    elif("Krajinovi" in row[key] and "F." in row[key]):
                        red.append("Krajinovic F.")
                    elif("Kruni" in row[key] and "A." in row[key]):
                        red.append("Krunic A.")
                    elif("Lajovi" in row[key] and "D." in row[key]):
                        red.append("Lajovic D.")
                    elif("Lu" in row[key] and "Baroni M." in row[key]):
                        red.append("Lucic Baroni M.")
                    elif("M.Pavi" in row[key] and "Venus" in row[key]):
                        red.append("M.Pavic/Venus")
                    elif("Deli" in row[key] and "M." in row[key]):
                        red.append("M.Delic")
                    elif("Pavi" in row[key] and "M." in row[key]):
                        red.append("M.Pavic")
                    elif("ili" in row[key] and "Ma." in row[key]):
                        red.append("Ma.Cilic")
                    elif("Marti" in row[key] and "Vogt" in row[key]):
                        red.append("Martic/Vogt")
                    elif("Marti" in row[key] and "P." in row[key]):
                        red.append("Martic P.")
                    elif("Mekti" in row[key] and "N." in row[key]):
                        red.append("Mektic N.")
                    elif("okovi" in row[key] and "N." in row[key]):
                        red.append("N.Djokovic")
                    elif("Savi" in row[key] and "A." in row[key]):
                        red.append("Savic A.")
                    elif("Schwartzman" in row[key] and "D." in row[key]):
                        red.append("Schwartzman D.S.")
                    elif("Tipsarevi" in row[key] and "J." in row[key]):
                        red.append("Tipsarevic J.")
                    elif("Veki" in row[key] and "D." in row[key]):
                        red.append("Vekic D.")
                    elif("ere L." in row[key]):
                        red.append("Djere L.")
                    elif("ori" in row[key] and "B." in row[key]):
                        red.append("Coric B.")
                    elif("emlja G." in row[key]):
                        red.append("Zemlja G.")
                    elif("etki" in row[key] and "A." in row[key]):
                        red.append("Setkic A.")
                    elif("kugor" in row[key] and "F." in row[key]):
                        red.append("Skugor F.")
                    elif("ili" in row[key] and "/Troicki" in row[key]):
                        red.append("Cilic/Troicki")
                    elif("Èaèiæ N." in row[key]):
                        red.append("Cacic N.")
                    
                    
                    
                    
                    
                    else:
                        red.append(row[key])


                else:
                    red.append(row[key])  

            #if (imaNeASCIIuRedu):
             #   print(red)
            redovi_csv_datoteke.append(red)

    print(setZamjenjenihIgraca)
    print("\nASCII igraci koji nisu u sviIgraci.csv")
    print(setASCIIigraca)
    print("\nneASCII igraci koji nisu u sviIgraci.cv")
    for i in sorted(setNeASCIIigraca):
        print(i)

    return redovi_csv_datoteke, setNeASCIIigraca


def upisi_u_novu_csv_datoteku(path, lista_odgovarajucih_redova, counter):
    path = 'promjenjenaImena/' + path

    try:

        with open(path, 'w', encoding = 'ISO-8859-1') as csvfile:
            writer = csv.writer(csvfile)

            if (counter == 0):
                writer.writerow(CSV_COLUMNS_0)
            else:
                writer.writerow(CSV_COLUMNS)
            
            for red in lista_odgovarajucih_redova:
                writer.writerow(red)

    except IOError:
        print("I/O Error")




def main():
    counter = 0

    rjecnikZamjene = rjecnik_imena_za_zamjenu()
    set_svih_neASCII_igraca = set()
    for line in sys.stdin:
        path = line.strip()
        print("\n-------------------------------------------------------------------------------------------------")
        print(path)

        pomLista = lista_redova_s_ispravljenim_imenima(path, rjecnikZamjene)   #prvo što funkcija vraća je lista svih ispravljenih redova datoteke, a onda set svih neASCII igraca
        dobri_redovi = pomLista[0]
        neASCII_igraci_u_tablici = pomLista[1]
        
        for i in neASCII_igraci_u_tablici:
            set_svih_neASCII_igraca.add(i)

        upisi_u_novu_csv_datoteku(path, dobri_redovi, counter)

        counter += 1

    print("\n\n")
    for i in sorted(set_svih_neASCII_igraca):
        print(i + ",False,")
main()   

# Pokretanje:
# python zamjena_imena_igraca.py < data.txt