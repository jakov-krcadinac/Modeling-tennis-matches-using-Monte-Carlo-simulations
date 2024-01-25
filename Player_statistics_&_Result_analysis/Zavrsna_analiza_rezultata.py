import csv
from collections import defaultdict
import sys

# Program provjerava koliko određena tablica ima mečeva


def lista_relevantnih_podataka(path):

    lista_rel_data = []   # varijabla u koju spremam redove s ispravljenim SporteventID-jem.  

    with open(path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        for row in csv_reader:

            recnik = {}
            
            if(row["Dinamicki_Monte_Carlo_pobjednik"] != "X"):
                recnik["igrac1"] = row["Igrac1"]
                recnik["igrac2"] = row["Igrac2"]
                recnik["pobjednik"] = row["Pobjednik"]
                recnik["din_winner"] = row["Dinamicki_Monte_Carlo_pobjednik"]
                recnik["din_p"] = row["Dinamicki_Monte_Carlo_pobjednik_p"]
                recnik["klas_winner"] = row["Klasicni_Monte_Carlo_pobjednik"]
                recnik["klas_p"] = row["Klasicni_Monte_Carlo_pobjednik_p"]
                recnik["din_umor_winner"] = row["Dinamicki_Monte_Carlo_pobjednik_samo_umor"]
                recnik["din_umor_p"] = row["Dinamicki_Monte_Carlo_pobjednik_samo_umor_p"]

                lista_rel_data.append(recnik)




    return lista_rel_data


def main():

    rel_data = lista_relevantnih_podataka("Projekt R/pobjednici.csv")
    broj_meceva = len(rel_data)
    print(broj_meceva)

    broj_pogodjenih_meceva_din = 0
    broj_pogodjenih_meceva_klas = 0
    broj_pogodjenih_meceva_din_umor = 0
    broj_fulanih_din = 0
    broj_jace_fulanih_din = 0
    broj_fulanih_klas = 0
    broj_jace_fulanih_klas = 0
    broj_fulanih_din_umor = 0
    broj_jace_fulanih_din_umor = 0

    broj_pogodjenih_s_p_bar_60_din = 0
    broj_pogodjenih_s_p_bar_60_klas = 0
    broj_pogodjenih_s_p_bar_60_din_umor = 0
    broj_fulanih_s_p_bar_60_din = 0
    broj_fulanih_s_p_bar_60_klas = 0
    broj_fulanih_s_p_bar_60_din_umor = 0


    broj_pogodjenih_s_p_bar_70_din = 0
    broj_pogodjenih_s_p_bar_70_klas = 0
    broj_pogodjenih_s_p_bar_70_din_umor = 0
    broj_fulanih_s_p_bar_70_din = 0
    broj_fulanih_s_p_bar_70_klas = 0
    broj_fulanih_s_p_bar_70_din_umor = 0

    for rjecnik in rel_data:
        #print(rjecnik)
        if (rjecnik["pobjednik"] == rjecnik["din_winner"]):
            broj_pogodjenih_meceva_din += 1
        else:
            broj_fulanih_din += 1
            if (rjecnik["pobjednik"] != rjecnik["klas_winner"]):
                if( float(rjecnik["din_p"]) > float(rjecnik["klas_p"])):
                    broj_jace_fulanih_din += 1
                elif(float(rjecnik["din_p"]) < float(rjecnik["klas_p"])):
                    broj_jace_fulanih_klas += 1
        
        if (rjecnik["pobjednik"] == rjecnik["klas_winner"]):
            broj_pogodjenih_meceva_klas += 1
        else:
            broj_fulanih_klas += 1

        if (rjecnik["pobjednik"] == rjecnik["din_umor_winner"]):
            broj_pogodjenih_meceva_din_umor += 1
        else:
            broj_fulanih_din_umor += 1

        # TESTIRANJE PRECIZNOSTI KADA JE SIMULACIJA 60% ILI VIŠE SIGURNA U POBJEDU JEDNOG IGRAČA
        
        if (float(rjecnik["din_p"]) >= 0.6):
            if (rjecnik["pobjednik"] == rjecnik["din_winner"]):
                broj_pogodjenih_s_p_bar_60_din += 1
            else:
                #print(rjecnik["pobjednik"], "Dinamicni pobjednik i njegov p:", rjecnik["din_winner"], rjecnik["din_p"], "   klasicni pobjednik i njegov p:",  rjecnik["klas_winner"], rjecnik["klas_p"])
                broj_fulanih_s_p_bar_60_din += 1

        if (float(rjecnik["klas_p"]) >= 0.6):
            if (rjecnik["pobjednik"] == rjecnik["klas_winner"]):
                broj_pogodjenih_s_p_bar_60_klas += 1
            else:
                broj_fulanih_s_p_bar_60_klas += 1
        
        if (float(rjecnik["din_umor_p"]) >= 0.6):
            if (rjecnik["pobjednik"] == rjecnik["din_umor_winner"]):
                broj_pogodjenih_s_p_bar_60_din_umor += 1
            else:
                broj_fulanih_s_p_bar_60_din_umor += 1


        # TESTIRANJE PRECIZNOSTI KADA JE SIMULACIJA 70% ILI VIŠE SIGURNA U POBJEDU JEDNOG IGRAČA

        if (float(rjecnik["din_p"]) >= 0.7):
            if (rjecnik["pobjednik"] == rjecnik["din_winner"]):
                broj_pogodjenih_s_p_bar_70_din += 1
            else:
                broj_fulanih_s_p_bar_70_din += 1


        if (float(rjecnik["klas_p"]) >= 0.7):
            if (rjecnik["pobjednik"] == rjecnik["klas_winner"]):
                broj_pogodjenih_s_p_bar_70_klas += 1
            else:
                broj_fulanih_s_p_bar_70_klas += 1

        if (float(rjecnik["din_umor_p"]) >= 0.7):
            if (rjecnik["pobjednik"] == rjecnik["din_umor_winner"]):
                broj_pogodjenih_s_p_bar_70_din_umor += 1
            else:
                broj_fulanih_s_p_bar_70_din_umor += 1

        

    
    print("broj meceva koje je uspješno predvidio dinamicki Monte Carlo:", broj_pogodjenih_meceva_din)
    print("broj meceva koje je fulao dinamicki Monte Carlo:", broj_fulanih_din)
    print()
    print("broj meceva koje je uspješno predvidio klasicni Monte Carlo:", broj_pogodjenih_meceva_klas)
    print("broj meceva koje je fulao klasicni Monte Carlo:", broj_fulanih_klas)
    print()
    print("broj meceva koje je jače fulao dinamicki Monte Carlo:", broj_jace_fulanih_din)
    print("broj meceva koje je jače fulao klasicni Monte Carlo:", broj_jace_fulanih_klas)
    print()
    print("broj meceva koje je uspješno predvidio dinamicni Monte Carlo koji uzima u obzir samo umor:", broj_pogodjenih_meceva_din_umor)
    print("broj meceva koje je fulao dinamicni Monte Carlo koji uzima u obzir samo umor:", broj_fulanih_din_umor)
    print()

    print("broj mečeva u kojima je p dinamičkog Monte Carla bio > 0.6 i pogodio je:", broj_pogodjenih_s_p_bar_60_din)
    print("broj mečeva u kojima je p dinamičkog Monte Carla bio > 0.6 i fulao je:", broj_fulanih_s_p_bar_60_din)
    print()
    print("broj mečeva u kojima je p klasičnog Monte Carla bio > 0.6 i pogodio je:", broj_pogodjenih_s_p_bar_60_klas)
    print("broj mečeva u kojima je p klasičnog Monte Carla bio > 0.6 i fulao je:", broj_fulanih_s_p_bar_60_klas)
    print()
    print("broj mečeva u kojima je p dinamičnog Monte Carla koji uzima u obzir samo umor bio > 0.6 i pogodio je:", broj_pogodjenih_s_p_bar_60_din_umor)
    print("broj mečeva u kojima je p dinamičnog Monte Carla koji uzima u obzir samo umor bio > 0.6 i fulao je:", broj_fulanih_s_p_bar_60_din_umor)
    print()

    print("broj mečeva u kojima je p dinamičkog Monte Carla bio > 0.7 i pogodio je:", broj_pogodjenih_s_p_bar_70_din)
    print("broj mečeva u kojima je p dinamičkog Monte Carla bio > 0.7 i fulao je:", broj_fulanih_s_p_bar_70_din)
    print()
    print("broj mečeva u kojima je p klasičnog Monte Carla bio > 0.7 i pogodio je:", broj_pogodjenih_s_p_bar_70_klas)
    print("broj mečeva u kojima je p klasičnog Monte Carla bio > 0.7 i fulao je:", broj_fulanih_s_p_bar_70_klas)
    print()
    print("broj mečeva u kojima je p dinamičnog Monte Carla koji uzima u obzir samo umor bio > 0.7 i pogodio je:", broj_pogodjenih_s_p_bar_70_din_umor)
    print("broj mečeva u kojima je p dinamičnog Monte Carla koji uzima u obzir samo umor bio > 0.7 i fulao je:", broj_fulanih_s_p_bar_70_din_umor)
    print()








main()   

# Pokretanje:
# python uredjivanje_sporteventID.py < data2.txt
