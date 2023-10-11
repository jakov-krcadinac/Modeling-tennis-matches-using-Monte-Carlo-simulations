import csv
from collections import defaultdict
import sys

BROJ_MECEVA = dict()
CSV_COLUMNS = ['SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']
CSV_COLUMNS_0 = ['No', 'SportEventID', 'EventTime', 'Home', 'Away', 'When', 'Period', 'Result',
'Minute', 'BetStatus', 'Closed', 'BetStopReason', 'InPlay']


def izbaci_meceve_bez_zavrsetka(path, counter):
    zavrseni_mecevi = set()
    with open(path, encoding = 'ISO-8859-1') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ';')
        for row in csv_reader:
            if "Z" in row["Period"] and not ("/" in row["Home"] ):
                if (counter <= 3 and counter > 0):
                    zavrseni_mecevi.update([row['SportEventID'][2:-1]])
                else:
                    zavrseni_mecevi.update([row['SportEventID']])

    with open(path, encoding = 'ISO-8859-1') as csv_file:
        mecevi = defaultdict(dict)
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            if (len(row['Period'].split()) != 1):
                continue
            if (counter <= 3 and counter > 0):
                id = row['SportEventID'][2:-1]
            else:
                id = row["SportEventID"]
            
            if id in zavrseni_mecevi:
                mecevi[id][row["When"]] = row

    return mecevi
            

def broji_meceve(mecevi):
    
    for mec in mecevi:
        for date in mecevi[mec]:
            home = mecevi[mec][date]['Home']
            away = mecevi[mec][date]['Away']

            BROJ_MECEVA[home] = BROJ_MECEVA.get(home, 0) + 1
            BROJ_MECEVA[away] = BROJ_MECEVA.get(away, 0) + 1

            break

def filtriraj_po_broju_meceva():
    maknutiIgraci = set()
    for name, broj_meceva in BROJ_MECEVA.items():
        if(broj_meceva <= 10):
            maknutiIgraci.update([name])

    return maknutiIgraci

            
def izbaci_visestruke_rezultate(mecevi):
    for idMeca in mecevi:
        prijasnji_rez = ''
        new = True
        for timestamp in sorted(mecevi[idMeca].keys()):
            if (prijasnji_rez == '' and new):
                prijasnji_rez = mecevi[idMeca][timestamp]['Result']
                new = False
            elif (prijasnji_rez == mecevi[idMeca][timestamp]['Result']):
                del mecevi[idMeca][timestamp]
            else:
                prijasnji_rez = mecevi[idMeca][timestamp]['Result']

    return mecevi

def upisi_u_novu_csv_datoteku(path, mecevi, counter):
    path = 'filtrirani/' + path

    try:
        with open(path, 'w', encoding = 'ISO-8859-1') as csvfile:
            if (counter == 0):
                writer = csv.DictWriter(csvfile, fieldnames = CSV_COLUMNS_0)
            else:
                writer = csv.DictWriter(csvfile, fieldnames = CSV_COLUMNS)
            
            writer.writeheader()

            for data in mecevi:
                for key in sorted(mecevi[data].keys()):
                    writer.writerow(mecevi[data][key])

    except IOError:
        print("I/O Error")


def main():
    counter = 0
    for line in sys.stdin:
        path = line.strip()

        print(path)

        mecevi = izbaci_meceve_bez_zavrsetka(path, counter)
        broji_meceve(mecevi)
        mecevi = izbaci_visestruke_rezultate(mecevi)

        upisi_u_novu_csv_datoteku(path, mecevi, counter)

        counter += 1

    maknuti_igraci = filtriraj_po_broju_meceva()

    for igrac in maknuti_igraci:
        print(igrac)

main()

#pokretanje programa: cat .\data.txt | python .\ciscenje.py
