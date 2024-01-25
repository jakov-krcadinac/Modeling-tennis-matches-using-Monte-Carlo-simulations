import csv
from collections import defaultdict
import sys

CSV_COLUMNS_0 = ['No', 'SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']

CSV_COLUMNS = ['SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']


# NAPOMENA: funkcija radi samo se u folderu nalazi folder "dataset" koji ima tablice 'competitionID.csv' i 'competitions.csv' 
# - opis funkcije -
    # promatrajući tablicu 'competitions.csv', ako je turnir s određenim CompetitionID-jem WTA ili ATP ili Grand Slam, njegov se CompetitionID dodaje u set 'ATP_i_WTA_turniri'.
    # Nakon toga promatramo tablicu 'competitionID.csv' u kojoj se za svaki meč nalazi njegov SportEventID i CompetitionID turnira na kojem se igrao meč 
    # Ako se CompetitionID nalazi u setu 'ATP_i_WTA_turniri', doodajemo kljuc(SportEventID)-vrijednost(CompetitionID) u rjecnik 'dict_sportevent_competition'
    # koji funkcija vraca
def rjecnik_sa_odgovarajucim_mecevima():
    sportevent_competition_path = "dataset/competitionID.csv"
    competitions_path = "dataset/competitions.csv"

    dict_sportevent_competition = defaultdict(dict)     #riječnik u koji ću spremati kljuc(SportEventID)-vrijednost(CompetitionID) 
                                                        # ako sportevent pripada turniru WTA ili ATP razine

    ATP_i_WTA_turniri = set()      #set u koji spremam CompetitionID-jeve svih turnira koji su ATP ili WTA

    with open(competitions_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ';')    # competitionID tablica nije ociscena pa je delimiter ';'
        
        for row in csv_reader:
            # Grand Slamovi se nalaze u nekoliko redaka u kojima ne piše nužno ATP ili WTA pa treba posebno provjeriti 
            # nalazi li se ime Grand Slama u nazivu turnira
            if (("ATP" in row["Name"]) or ("WTA" in row["Name"]) or 
                ("ROLAND GARROS" in row["Name"]) or ("WIMBLEDON" in row["Name"]) or     
                ("AUSTRALIAN OPEN" in row["Name"]) or ("US OPEN" in row["Name"])):      

                print(row["CompID"] + " je id tunira " + row["Name"])
                ATP_i_WTA_turniri.add(row["CompID"])

    # što se tiče tablice "competitions1.csv", ona sadrži potpuno iste WTA i ATP turnire kao i tablica "competitons.csv".
    # provjerio sam to programski, ali sam izbrisao taj kod radi jednostavnosti.

    # usporedi nalazi li se CompetitionID u setu i ako da onda dodaj u rječnik koji će funkcija vratiti 
    with open(sportevent_competition_path, encoding = 'ISO-8859-1') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = ';')    # competitionID tablica nije ociscena pa je delimiter ';'
        for row in csv_reader:
            if row["CompetitionID"] in ATP_i_WTA_turniri:
                dict_sportevent_competition[row["SportEventID"]] = row["CompetitionID"]
                        #print(row["SportEventID"] + " je u ATP ili WTA turniru : " + row["CompetitionID"])     PROVJERA

    return dict_sportevent_competition



#funkcija koja izbacuje turnire koji nisu WTA ili ATP. Funkcija vraća listu koja sadrži sve redove koji pripadaju mečevima sa ATP ili WTA turnira
def izbacivanje_nevaznih_turnira(path, ATP_i_WTA_SporteventIDs):
    pravi_path = "filtrirani/" + path

    redovi_csv_datoteke = []   # varijabla u koju spremam SAMO redove koji pripadaju mečevima sa ATP ili WTA turnira

    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        for row in csv_reader:

            if row["SportEventID"] in ATP_i_WTA_SporteventIDs.keys():
                red = []

                for key in row.keys():
                    red.append(row[key])

                redovi_csv_datoteke.append(red)
    
    return redovi_csv_datoteke


def upisi_u_novu_csv_datoteku(path, lista_odgovarajucih_redova, counter):
    path = 'filtrirani_final/' + path

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
    ATP_i_WTA_SporteventIDs = rjecnik_sa_odgovarajucim_mecevima()

    for line in sys.stdin:
        path = line.strip()

        print(path)

        dobri_redovi = izbacivanje_nevaznih_turnira(path, ATP_i_WTA_SporteventIDs)   # lista koj sadrži samo redove .csv datoteke sa podacima o turniru koji je ATP ili WTA razine

        upisi_u_novu_csv_datoteku(path, dobri_redovi, counter)

        counter += 1

    
# Pokretanje:
# python izbacivanjeNevaznihTurnira.py < data.txt


main()