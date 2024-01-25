import csv
from collections import defaultdict
import sys

# NAPOMENA: program je brzinski rađen i 30% toga je copy pasteano i nepotrebno, ali bitno da funkcionira. 
#           ima vrlo jednostavnu svrhu i trebalo ga je samo jednom pokrenuti da se počisti vrlo mali dio date,
#           pa smatram da nije bitno daljnje optimiziranje.

CSV_COLUMNS_0 = ['No', 'SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']

CSV_COLUMNS = ['SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']

# funkcija koja vraća listu sa očišćenim redovima .csv datoteka (promjenjen je SportEventID u 7-znamenkasti broj)
def lista_ispravljenih_redova(path):
    pravi_path = "filtrirani/" + path

    redovi_csv_datoteke = []   # varijabla u koju spremam redove s ispravljenim SporteventID-jem.  

    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        for row in csv_reader:

            if ";" in row["SportEventID"]:
                red = []
                pravi = row["SportEventID"][2:]     #SportEventID je originalno bio formata ';"1423867' umjesto '1423867' i to treba ispraviti
                red.append(pravi)

                for key in row.keys():
                    if key != "SportEventID":
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
    counter = 2

    for line in sys.stdin:
        path = line.strip()

        print(path)

        dobri_redovi = lista_ispravljenih_redova(path)   

        upisi_u_novu_csv_datoteku(path, dobri_redovi, counter)

        counter += 1

main()   

# Pokretanje:
# python uredjivanje_sporteventID.py < data2.txt