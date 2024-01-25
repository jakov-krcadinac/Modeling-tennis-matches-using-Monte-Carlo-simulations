import csv
from collections import defaultdict
import sys


CSV_COLUMNS_0 = ['No', 'SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']

CSV_COLUMNS = ['SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']


def lista_SportEventIDjeva(path):
    pravi_path = "filtrirani_final/" + path

    svi_SportEventID = []   # varijabla u koju spremam redove s ispravljenim SporteventID-jem.  

    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        for row in csv_reader:

            svi_SportEventID.append(row["SportEventID"])

    return svi_SportEventID


def main():

    lista_2015 = lista_SportEventIDjeva("tenis_2015_sportevent.csv")
    lista_2015_i = []

    for line in sys.stdin:
        path = line.strip()

        print(path)

        lista_2015_pomocna = lista_SportEventIDjeva(path)   
        for i in lista_2015_pomocna:
            lista_2015_i.append(i)

    print("Svi koji su u tenis_2015_sportevent, a nisu u ", path, ": ")
    print(list(set(lista_2015) - set(lista_2015_i)))

    print("Svi koji su u tenis_2015_sportevent_1-3, a nisu u tenis_2015_sportevent:")
    retList = list(set(lista_2015_i) - set(lista_2015))
    print(retList)
    print(len(retList))

main()   

# Pokretanje:
# python uredjivanje_sporteventID.py < data2.txt


l1=[1,2,3]
l2=[3,4,5]
print(list(set(l1) - set(l2)))