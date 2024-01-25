import csv
from collections import defaultdict
import sys


CSV_COLUMNS = ['SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']

def ASCIIime(ime):  #Vraca True ako ime sadrzi samo ASCII znakove
    retVal = True
    for i in ime:
        if ( (i>="a" and i<="z") or (i>="A" and i<="Z") or (i==" ") or (i==".") or (i=="/") or (i=="-")):
            continue
        else:
            retVal=False
    return retVal

def lista_dugog_dijela_meca(path):
    pravi_path = "Projekt R/filtriraniIzbaceno/" + path

    svi_redovi = []   # varijabla u koju spremam redove s ispravljenim SporteventID-jem.  
    
    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        
        for row in csv_reader:

            if( (row["Period"] in ["3.set", "4.set", "5.set"]) or (row["Period"][0] == "Z" and row["Result"].count("-") > 2)):
                
                red_recnik = {}

                red_recnik["SportEventID"] = row["SportEventID"]
                red_recnik["Home"] = row["Home"]
                red_recnik["Away"] = row["Away"]
                red_recnik["Period"] = row["Period"]
                red_recnik["Result"] = row["Result"]

                svi_redovi.append(red_recnik)        
                
    return svi_redovi


def lista_cijelog_meca(path):
    pravi_path = "Projekt R/filtriraniIzbaceno/" + path

    svi_redovi = []   # varijabla u koju spremam redove s ispravljenim SporteventID-jem.  
    
    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        
        for row in csv_reader:
            
            if( (row["Period"] != "Prekid")):

                red_recnik = {}

                red_recnik["SportEventID"] = row["SportEventID"]
                red_recnik["Home"] = row["Home"]
                red_recnik["Away"] = row["Away"]
                red_recnik["Period"] = row["Period"]
                red_recnik["Result"] = row["Result"]

                svi_redovi.append(red_recnik)        
                
    return svi_redovi

def lista_prva_dva_seta_meca(path):
    pravi_path = "Projekt R/filtriraniIzbaceno/" + path

    svi_redovi = []   # varijabla u koju spremam redove s ispravljenim SporteventID-jem.  
    
    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        
        for row in csv_reader:

            if( (row["Period"] in ["1.set", "2.set"])):
                
                red_recnik = {}

                red_recnik["SportEventID"] = row["SportEventID"]
                red_recnik["Home"] = row["Home"]
                red_recnik["Away"] = row["Away"]
                red_recnik["Period"] = row["Period"]
                red_recnik["Result"] = row["Result"]

                svi_redovi.append(red_recnik)        
                
    return svi_redovi

# Funkcija za dodatno ispitivanje ulazi li meč u Tiebreaker kada je rezultat 6-6 u setovima
def jel_tiebreaker(trenutni_rez, iduci_rez):
    if ("Pr" in trenutni_rez[0] or "Pr" in trenutni_rez[1] or "Pr" in iduci_rez[0] or "Pr" in iduci_rez[1]):
        return False
    if(int(iduci_rez[0].replace('*', '')) - int(trenutni_rez[0].replace('*', '')) > 2 or 
        int(iduci_rez[1].replace('*', '')) - int(trenutni_rez[1].replace('*', '')) > 2 or
        abs(int(trenutni_rez[1].replace('*', '')) - int(trenutni_rez[0].replace('*', '')) > 13)):
        return False
    return True

# funkcija vraća rječnik p_igraca sa imenima igrača i statistikama o broju dobivenih servisa itd.
def p_igraca(lista_meceva):

    p_igraca = {}       #rečnik kojem su ključevi imena igrača, a value lista [broj dobivenih servisa, broj servisa]
    
    for i in range(len(lista_meceva)-1):
        
        if ("*" in lista_meceva[i]["Result"]):

            if ( lista_meceva[i+1]["SportEventID"] == lista_meceva[i]["SportEventID"] ):
                trenutni_rez = lista_meceva[i]["Result"].split(" ")[len(lista_meceva[i]["Result"].split(" ")) - 1].split("-")
                iduci_rez = lista_meceva[i+1]["Result"].split(" ")[len(lista_meceva[i+1]["Result"].split(" ")) - 1].split("-")
                
                if (lista_meceva[i]["Home"] not in p_igraca.keys()):
                    p_igraca[lista_meceva[i]["Home"]] = [0, 0, 0, 0]  # prvi broj u listi je broj osvojenih poena kad je igrač servirao,
                                                                      # drugi broj u listi je broj puta kad je igrač servirao
                                                                      # treći broj u listi je broj poena kada je igrač osvojio poen, a nije servirao nego primao servis
                                                                      # četvrti broj u listi je ukupan broj poena u kojima je igrač primao tuđi servis
                if (lista_meceva[i]["Away"] not in p_igraca.keys()):
                    p_igraca[lista_meceva[i]["Away"]] = [0, 0, 0, 0]

                if ("*" in trenutni_rez[0]):    # Home igrač servira
                    p_igraca[lista_meceva[i]["Home"]][1] += 1   # povećavam broj puta kad je Home igrač servirao
                    p_igraca[lista_meceva[i]["Away"]][3] += 1   # povećavam ukupan broj poena u kojima je igrač Away primao tuđi servis
                    
                    #provjera za Karlovica
                    #if("Karlovi" in lista_meceva[i]["Home"]):
                    #    print(lista_meceva[i]["Home"], lista_meceva[i]["Away"], lista_meceva[i]["Period"], lista_meceva[i]["Result"], trenutni_rez)
                    #    print(p_igraca[lista_meceva[i]["Home"]], p_igraca[lista_meceva[i]["Away"]])

                    if (lista_meceva[i]["Result"].split(" ")[-2] == "6-6" and jel_tiebreaker(trenutni_rez, iduci_rez)):  # igra se TIEBREAKER
                        
                        if ("*" not in ''.join(iduci_rez)):  #slučaj kada je u idućem redu Tiebreaker završio
                            if(int(trenutni_rez[1].replace('*', '')) > int(trenutni_rez[0].replace('*', ''))):  # ako je neposredno prije završetka Tiebreaka igrač koji ne servira 
                                                                                                                # imao više bodova on je pobjedio
                                p_igraca[lista_meceva[i]["Away"]][2] += 1
                            else:
                                p_igraca[lista_meceva[i]["Home"]][0] += 1

                        elif (int(iduci_rez[0].replace('*', '')) == int(trenutni_rez[0].replace('*', ''))+1):  
                            p_igraca[lista_meceva[i]["Home"]][0] += 1

                        else:
                            p_igraca[lista_meceva[i]["Away"]][2] += 1
                        #print("igra se tiebreak", lista_meceva[i]["Result"])
                        #print(p_igraca[lista_meceva[i]["Home"]], p_igraca[lista_meceva[i]["Away"]])
                        
                    elif ( trenutni_rez[0] in ["40*", "*40"]):
                        if (trenutni_rez[1] == "Pr" and ("*" not in iduci_rez[0]) ):
                            p_igraca[lista_meceva[i]["Away"]][2] += 1   # povećavam broj dobivenih primljenih servisa away igrača koji nije na servisu jer je uspješno brejkao servisera
                        elif (trenutni_rez[1] == "Pr" and iduci_rez[0] in ["40*", "*40"]):   # rezultat je 40*-Pr, nakon toga Home servira i osvaja poen pa je rezultat opet 40*-40
                            p_igraca[lista_meceva[i]["Home"]][0] += 1
                        elif ("*" not in iduci_rez[0]):   # home igrač u sljedećem rezultatu više nije na servisu, znači da je osvojio poen
                            p_igraca[lista_meceva[i]["Home"]][0] += 1   # povećavam broj dobivenih servisa home igrača
                        elif (iduci_rez[0] in ["40*", "*40"]):
                            p_igraca[lista_meceva[i]["Away"]][2] += 1   # povećavam broj dobivenih primljenih servisa away igrača koji nije na servisu jer je osvojio poen
                        elif(iduci_rez[0] in ["Pr*", "*Pr"]):
                            p_igraca[lista_meceva[i]["Home"]][0] += 1   # znači da je trenutni rezultat 40*-40, sljedeći poen je dobio Home igrač i sad je Pr*-40

                    elif ( trenutni_rez[0] in ["Pr*", "*Pr"]):
                        if ("*" not in iduci_rez[0]):   # home igrač u sljedećem rezultatu više nije na servisu, znači da je osvojio poen
                            p_igraca[lista_meceva[i]["Home"]][0] += 1   # povećavam broj dobivenih servisa home igrača
                        elif (iduci_rez[0] in ["40*", "*40"]):
                            p_igraca[lista_meceva[i]["Away"]][2] += 1   # povećavam broj dobivenih primljenih servisa away igrača koji nije na servisu jer je osvojio poen i vratio Home igrača na 40*-40

                    elif ( trenutni_rez[0] in ["0*", "*0"] or trenutni_rez[0] in ["15*", "*15"] or trenutni_rez[0] in ["30*", "*30"]):     
                        if ( iduci_rez[0] == trenutni_rez[0]):  
                            p_igraca[lista_meceva[i]["Away"]][2] += 1   #ako se broj poena igrača koji servira nije promijenio u sljedećem servisu znači da je drugi igrač osvojio poen 
                        elif("*" not in iduci_rez[0]):
                            p_igraca[lista_meceva[i]["Away"]][2] += 1  # ako u idućem rezultatu Home koji trenutno servisira ima 0 poena znači da je trenutno
                                                                       # igrač Away na 40 bodova i u idućem rezultatu osvaja gejm 
                        else:
                            p_igraca[lista_meceva[i]["Home"]][0] += 1   # ako igrač ima neki drugi broj bodova onda je osvojio poen na trenutnom servisu

                elif ("*" in trenutni_rez[1]):    # Away igrač servira
                    p_igraca[lista_meceva[i]["Away"]][1] += 1   # povećavam broj puta kad je igrač servirao
                    p_igraca[lista_meceva[i]["Home"]][3] += 1   # povećavam ukupan broj poena u kojima je igrač Home primao tuđi servis
                    
                    # provjera za Karlovica 
                    #if("Karlovi" in lista_meceva[i]["Home"]):
                    #    print(lista_meceva[i]["Home"], lista_meceva[i]["Away"], lista_meceva[i]["Period"], lista_meceva[i]["Result"], trenutni_rez)
                    #    print(p_igraca[lista_meceva[i]["Home"]], p_igraca[lista_meceva[i]["Away"]])

                    if (lista_meceva[i]["Result"].split(" ")[-2] == "6-6" and jel_tiebreaker(trenutni_rez, iduci_rez)):  # igra se TIEBREAKER
                        if ("*" not in ''.join(iduci_rez)):     #slučaj kada je u idućem redu Tiebreaker završio
                            if(int(trenutni_rez[0].replace('*', '')) > int(trenutni_rez[1].replace('*', ''))):  # ako je neposredno prije završetka Tiebreaka igrač koji ne servira 
                                                                                                                # imao više bodova on je pobjedio
                                p_igraca[lista_meceva[i]["Home"]][2] += 1
                            else:
                                p_igraca[lista_meceva[i]["Away"]][0] += 1

                        elif (int(iduci_rez[1].replace('*', '')) == int(trenutni_rez[1].replace('*', ''))+1):  
                            p_igraca[lista_meceva[i]["Away"]][0] += 1

                        else:
                            p_igraca[lista_meceva[i]["Home"]][2] += 1
                        #print("igra se tiebreak", lista_meceva[i]["Result"])
                        #print(p_igraca[lista_meceva[i]["Home"]], p_igraca[lista_meceva[i]["Away"]])

                    elif ( trenutni_rez[1] == "40*"):

                        if (trenutni_rez[0] == "Pr" and ("*" not in iduci_rez[1]) ):
                            p_igraca[lista_meceva[i]["Home"]][2] += 1   # povećavam broj dobivenih primljenih servisa Home igrača koji nije na servisu jer je uspješno brejkao servisera
                        elif (trenutni_rez[0] == "Pr" and iduci_rez[1] == "40*"):   # rezultat je Pr-40*, nakon toga Away servira i osvaja poen pa je rezultat opet 40-40*
                            p_igraca[lista_meceva[i]["Away"]][0] += 1
                        elif ("*" not in iduci_rez[1]):   # home igrač u sljedećem rezultatu više nije na servisu, znači da je osvojio poen
                            p_igraca[lista_meceva[i]["Away"]][0] += 1   # povećavam broj dobivenih servisa away igrača
                        elif (iduci_rez[1] == "40*"):
                            p_igraca[lista_meceva[i]["Home"]][2] += 1   # povećavam broj dobivenih primljenih servisa home igrača koji nije na servisu jer je osvojio poen
                        elif(iduci_rez[1] == "Pr*"):
                            p_igraca[lista_meceva[i]["Away"]][0] += 1   # znači da je trenutni rezultat 40*-40, sljedeći poen je dobio Away igrač i rezultat je Pr*-40

                    elif ( trenutni_rez[1] == "Pr*"):
                        if ("*" not in iduci_rez[1]):   # Away igrač u sljedećem rezultatu više nije na servisu, znači da je osvojio poen
                            p_igraca[lista_meceva[i]["Away"]][0] += 1   # povećavam broj dobivenih servisa away igrača
                        elif (iduci_rez[1] == "40*"):
                            p_igraca[lista_meceva[i]["Home"]][2] += 1   # povećavam broj dobivenih primljenih servisa home igrača koji nije na servisu jer je osvojio poen i vratio Home igrača na 40*-40

                    elif ( trenutni_rez[1] == "0*" or trenutni_rez[1] == "15*" or trenutni_rez[1] == "30*"):     
                        if ( iduci_rez[1] == trenutni_rez[1]):  #ako se broj poena igrača koji servira nije promijenio u sljedećem servisu znači da je drugi igrač osvojio poen 
                             p_igraca[lista_meceva[i]["Home"]][2] += 1
                        elif("*" not in iduci_rez[1]):
                            p_igraca[lista_meceva[i]["Home"]][2] += 1  # ako u idućem rezultatu Away koji trenutno servisira ima 0 poena znači da je trenutno
                                                                       # igrač Home na 40 bodova i u idućem rezultatu osvaja gejm 
                        else:
                            p_igraca[lista_meceva[i]["Away"]][0] += 1   # ako igrač ima neki drugi broj bodova onda je osvojio poen na trenutnom servisu

                #print(lista_meceva[i]["Home"], lista_meceva[i]["Away"], lista_meceva[i]["Period"], lista_meceva[i]["Result"], trenutni_rez)
                #print(lista_meceva[i+1]["Period"], lista_meceva[i+1]["Result"], iduci_rez)
                #print(lista_meceva[i]["SportEventID"])
        
        #print(p_igraca)
    return p_igraca
        

def upisi_u_novu_csv_datoteku(rjecnik_cijeli_mec, rjecnik_prva_2_set, rjecnik_dugi_dio_meca):
    path = 'Projekt R/statistike/p_vjerojatnosti_igraca.csv'

    try:
        with open(path, 'w', encoding = 'ISO-8859-1') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(["Player", "CIJELI_MEC_osvojeni_poeni_kad_servira", "CIJELI_MEC_broj_servisa", "CIJELI_MEC_p", 
                                       "CIJELI_MEC_osvojeni_poeni_kad_prima_servis", "CIJELI_MEC_broj_primljenih_servisa", "CIJELI_MEC_p_kad_prima_servis", 
                                       "PRVA_2_SETA_osvojeni_poeni_kad_servira", "PRVA_2_SETA_broj_servisa", "PRVA_2_SETA_p", 
                                       "PRVA_2_SETA_osvojeni_poeni_kad_prima_servis", "PRVA_2_SETA_broj_primljenih_servisa", "PRVA_2_SETA_p_kad_prima_servis",
                                       "DUGI_DIO_MECA_osvojeni_poeni_kad_servira", "DUGI_DIO_MECA_broj_servisa", "DUGI_DIO_MECA_p", 
                                       "DUGI_DIO_MECA_osvojeni_poeni_kad_prima_servis", "DUGI_DIO_MECA_broj_primljenih_servisa", "DUGI_DIO_MECA_p_kad_prima_servis"])
            
            for kljuc in sorted(rjecnik_cijeli_mec.keys()):
                lista_za_upis = []
                lista_za_upis.append(kljuc) # dodaje se ime igraca

                # dodavanje CIJELI_MEC vrijednosti
                lista_za_upis.append(rjecnik_cijeli_mec[kljuc][0])
                lista_za_upis.append(rjecnik_cijeli_mec[kljuc][1])
                lista_za_upis.append(rjecnik_cijeli_mec[kljuc][0] / rjecnik_cijeli_mec[kljuc][1])   # dodaje se p - postotak osvojenih poena kada igrac servira
                lista_za_upis.append(rjecnik_cijeli_mec[kljuc][2])
                lista_za_upis.append(rjecnik_cijeli_mec[kljuc][3])
                lista_za_upis.append(rjecnik_cijeli_mec[kljuc][2] / rjecnik_cijeli_mec[kljuc][3])   # dodaje se p_kad_prima_servis - postotak osvojenih poena kada je igrac primao servis
                
                
                # dodavanje PRVA_2_SETA vrijednosti
                lista_za_upis.append(rjecnik_prva_2_set[kljuc][0])
                lista_za_upis.append(rjecnik_prva_2_set[kljuc][1])
                lista_za_upis.append(rjecnik_prva_2_set[kljuc][0] / rjecnik_prva_2_set[kljuc][1])   # dodaje se p - postotak osvojenih poena kada igrac servira
                lista_za_upis.append(rjecnik_prva_2_set[kljuc][2])
                lista_za_upis.append(rjecnik_prva_2_set[kljuc][3])
                lista_za_upis.append(rjecnik_prva_2_set[kljuc][2] / rjecnik_prva_2_set[kljuc][3])   # dodaje se p_kad_prima_servis - postotak osvojenih poena kada je igrac primao servis
                

                # dodavanje DUGI_DIO_MECA vrijednosti
                if (kljuc != "De Bakker T." and kljuc != "F.Mayer" and kljuc != "Hibino N." and kljuc != "Kontaveit A."     #postoje igrači koji niti u jednom meču nisu ušli u 3. set ili dalje. 
                    and kljuc != "Martic P." and kljuc != "Nishioka Y." and kljuc != "Paszek T." and kljuc != "R.Harrison"  # takve igrače svejedno zapisujemo u tablicu, ali im dajemo na svim mjestima
                    and kljuc != "S.Crawford" and kljuc != "Sakkari M." and kljuc != "Sevastova A." and kljuc != "Ta.Ito"    # dugog dijela meča rezultat 0
                    ):   
                    lista_za_upis.append(rjecnik_dugi_dio_meca[kljuc][0])
                    lista_za_upis.append(rjecnik_dugi_dio_meca[kljuc][1])
                    lista_za_upis.append(rjecnik_dugi_dio_meca[kljuc][0] / rjecnik_dugi_dio_meca[kljuc][1])   # dodaje se p - postotak osvojenih poena kada igrac servira
                    lista_za_upis.append(rjecnik_dugi_dio_meca[kljuc][2])
                    lista_za_upis.append(rjecnik_dugi_dio_meca[kljuc][3])
                    lista_za_upis.append(rjecnik_dugi_dio_meca[kljuc][2] / rjecnik_dugi_dio_meca[kljuc][3])   # dodaje se p_kad_prima_servis - postotak osvojenih poena kada je igrac primao servis

                else:
                    for i in range(6):
                        lista_za_upis.append(0)
                    

                writer.writerow(lista_za_upis)

    except IOError:
        print("I/O Error")

def main():

    sveTablice = ["tenis_2015_sportevent_1.csv", "tenis_2015_sportevent_2.csv", "tenis_2015_sportevent_3.csv",
                    "tenis_2016_01_sportevent.csv", "tenis_2016_02_sportevent.csv", "tenis_2016_03_sportevent.csv",
                    "tenis_2016_04_sportevent.csv", "tenis_2016_05_sportevent.csv", "tenis_2016_06_sportevent.csv",
                    "tenis_2016_07_sportevent.csv", "tenis_2016_08_sportevent.csv", "tenis_2016_09_sportevent.csv",
                    "tenis_2016_10_sportevent.csv", "tenis_2016_11_sportevent.csv"]

    DataTablice = ["tenis_2015_sportevent_1.csv", "tenis_2015_sportevent_2.csv", "tenis_2015_sportevent_3.csv",
                    "tenis_2016_01_sportevent.csv", "tenis_2016_02_sportevent.csv", "tenis_2016_03_sportevent.csv",
                    "tenis_2016_04_sportevent.csv", "tenis_2016_05_sportevent.csv"]


# RAČUNANJE P IGRACA IZ CIJELOG MECA ZA SVAKI MEC KOJI JE IGRAO

    svi_redovi = []

    for tablica in DataTablice:
        sviRedoviTablice = lista_cijelog_meca(tablica)
        for red in sviRedoviTablice:
            svi_redovi.append(red)

    #print("Dio meča koji je ušao u 3. set ili dalje za sve mečeve\n")

    #for i in svi_redovi:
    #    print(i)

    
    recnik_svih_igraca_cijeli_mec = p_igraca(svi_redovi) # rjecnik u koji su upisani svi igraci i njihove statistike

    print("statistike za igrace kad su usli u 1. i 2. set\n")
    for key in sorted(recnik_svih_igraca_cijeli_mec.keys()):
        print(key, recnik_svih_igraca_cijeli_mec[key])


    
# RAČUNANJE P_PRVA_2_SETA 

    svi_redovi_prva_dva_seta_meca = []

    for tablica in DataTablice:
        sviRedoviTablice = lista_prva_dva_seta_meca(tablica)
        for red in sviRedoviTablice:
            svi_redovi_prva_dva_seta_meca.append(red)

    #print("Dio meča koji je ušao u 3. set ili dalje za sve mečeve\n")

    #for i in svi_redovi_prva_dva_seta_meca:
     #   print(i)

    recnik_svih_igraca_prva_2_seta = p_igraca(svi_redovi_prva_dva_seta_meca) # rjecnik u koji su upisani svi igraci i njihove statistike

    print("statistike za igrace kad su usli u 1. i 2. set\n")
    for key in sorted(recnik_svih_igraca_prva_2_seta.keys()):
        print(key, recnik_svih_igraca_prva_2_seta[key])

    
# RAČUNANJE P_KAD_JE_UMORAN ZA SVE REDOVE TABLICA KOJI SU U 3., 4. ILI 5. SETU

    svi_redovi_dugog_dijela_meca = []

    for tablica in DataTablice:
        sviRedoviTablice = lista_dugog_dijela_meca(tablica)
        for red in sviRedoviTablice:
            svi_redovi_dugog_dijela_meca.append(red)

    #print("Dio meča koji je ušao u 3. set ili dalje za sve mečeve\n")

    #for i in svi_redovi_dugog_dijela_meca:
    #    print(i)

    
    recnik_svih_igraca_dugi_dio_meca = p_igraca(svi_redovi_dugog_dijela_meca) # rjecnik u koji su upisani svi igraci i njihove statistike

    print("statistike za igrace kad su usli u 3., 4. ili 5. set")
    for key in sorted(recnik_svih_igraca_dugi_dio_meca.keys()):
        print(key, recnik_svih_igraca_dugi_dio_meca[key])

    upisi_u_novu_csv_datoteku(recnik_svih_igraca_cijeli_mec, recnik_svih_igraca_prva_2_seta, recnik_svih_igraca_dugi_dio_meca)
    

    



    """  DIO PROGRAMA KOJI KONTROLIRA POSTOJE LI neASCII IGRAČI U DATASETU

    setsvihRedoviPromjenjenaImena = set()

    #provjera za koristenje dijela imena u key[row]
    setSvihInstanci = set()

    print("Pocinjem provjeru \n")
    for tablica in DataTablice:
        sviRedoviTablice = lista_cijelog_meca(tablica)
        for red in sviRedoviTablice:
            if (not ASCIIime(red["Home"])):
                setsvihRedoviPromjenjenaImena.add(red["Home"])
            if (not ASCIIime(red["Away"])):
                setsvihRedoviPromjenjenaImena.add(red["Away"])

            if ("Èaèiæ N." in red["Away"] and " " in red["Away"]):    #radimo provjeru
                setSvihInstanci.add(red["Away"] + red["Home"] + tablica)
            if("Èaèiæ N." in red["Home"] and " " in red["Home"]):       
                setSvihInstanci.add(red["Home"] + red["Away"] + tablica)
    
    for i in sorted(setsvihRedoviPromjenjenaImena):
        print(i)

    print()
    print(setSvihInstanci)
    
    """ 
    
    



main()   
