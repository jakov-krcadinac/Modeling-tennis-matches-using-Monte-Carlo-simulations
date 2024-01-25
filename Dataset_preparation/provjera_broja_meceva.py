import csv
from collections import defaultdict
import sys

# Program provjerava koliko određena tablica ima mečeva


def lista_SportEventIDjeva(path):
    pravi_path = path

    svi_SportEventID = set()   # varijabla u koju spremam redove s ispravljenim SporteventID-jem.  

    with open(pravi_path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    # u ociscenim .csv fileovima delimiter više nije ';' nego ','
        for row in csv_reader:

            svi_SportEventID.add(row["SportEventID"])

    return svi_SportEventID


def main():

    ukupni_broj_meceva = 0

    for line in sys.stdin:
        path = line.strip()

        set_svih_meceva_tablice = lista_SportEventIDjeva(path)  

        print(path, "ima ", len(set_svih_meceva_tablice), "meceva")

        ukupni_broj_meceva += len(set_svih_meceva_tablice)

    print("sve tablice zajedno imaju", ukupni_broj_meceva, "meceva")




        





main()   

# Pokretanje:
# python provjera_kolikoImaMeceva.py < izbacivanjeDuplicaData.txt
# python provjera_kolikoImaMeceva.py < data5.txt

