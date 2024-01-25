import csv
from collections import defaultdict
import sys

CSV_COLUMNS_0 = ['No', 'SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']

CSV_COLUMNS = ['SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']




#funkcija koja izbacuje turnire koji nisu WTA ili ATP. Funkcija vraća listu koja sadrži sve redove koji pripadaju mečevima sa ATP ili WTA turnira
def izbacivanje_duplih_redaka(path):
    pravi_path = "filtriraniIzbaceno/" + path

    redovi_csv_datoteke = []   # varijabla u koju spremam SAMO redove koji pripadaju mečevima sa ATP ili WTA turnira

    ret_recnik = {}

    ret_recnik["broj_redaka"] = 0
    ret_recnik["broj_duplica"] = 0

    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        
        for row in csv_reader:

            ret_recnik["broj_redaka"] += 1
            
            if (len(redovi_csv_datoteke) == 0):
                redovi_csv_datoteke.append(row)
            
            else:
                if (redovi_csv_datoteke[len(redovi_csv_datoteke)-1]["Result"] == row["Result"]):
                    #print(path, ret_recnik["broj_redaka"]*2+1)
                    #print(redovi_csv_datoteke[len(redovi_csv_datoteke)-1])
                    #print(row)
                    ret_recnik["broj_duplica"] += 1
                else:
                    redovi_csv_datoteke.append(row)


            #print(row)
    
    ret_recnik["redovi"] = redovi_csv_datoteke
    
    return ret_recnik


def upisi_u_novu_csv_datoteku(path, lista_odgovarajucih_redova):
    path = 'izbaceniDuplici/' + path

    try:

        with open(path, 'w', encoding = 'ISO-8859-1') as csvfile:
            writer = csv.writer(csvfile)

            
            writer.writerow(CSV_COLUMNS)
            
            for red in lista_odgovarajucih_redova:  # red je lista kljuceva svakog reda
                counter = 0
                lista = []
                for key in red:
                    if (counter == 0):
                        if (red[key] == ""):
                            continue
                        else:
                            lista.append(red[key])
                    else:
                        lista.append(red[key])
                    counter += 1
                writer.writerow(lista)

    except IOError:
        print("I/O Error")




def main():

    for line in sys.stdin:
        path = line.strip()

        print(path)

        rjecnik_izbacenih = izbacivanje_duplih_redaka(path)  
        
        print("broj redaka prije izbacivanja", rjecnik_izbacenih["broj_redaka"])
        print("broj duplih redova u tablici", rjecnik_izbacenih["broj_duplica"])
        print("broj redaka tablice nakon izbacivanja duplica", len(rjecnik_izbacenih["redovi"]))

        upisi_u_novu_csv_datoteku(path, rjecnik_izbacenih["redovi"])


    
# Pokretanje:
# python izbacivanje_duplih_redova.py < izbacivanjeDuplicaData.txt


main()