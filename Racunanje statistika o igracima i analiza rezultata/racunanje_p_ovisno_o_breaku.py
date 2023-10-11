import csv

OSVOJENI = dict()
IZGUBLJENI = dict()

def broji_osvojene_bodove(path):
    with open(path, encoding='ISO-8859-1') as csv_file:
        prev_result = ''
        breaked = 0

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            if row['Home'] not in OSVOJENI:
                OSVOJENI[row['Home']] = [0, 0]
                IZGUBLJENI[row['Home']] = [0, 0]
            if row['Away'] not in OSVOJENI:
                OSVOJENI[row['Away']] = [0, 0]
                IZGUBLJENI[row['Away']] = [0, 0]

            if (row['Period'] == "Prekid" or row['Period'] == "Zavrseno" or row['Period'] == "Zavr_eno"):
                prev_result = ''
                breaked = 0
                continue

            if row['Result'] == '':
                continue

            result = row['Result'].split(' ')
            breaks = result[-2].split('-')
            result = result[-1]
            result2 = result.split('-')

            if (breaks[0] == "0" and breaks[1] == "0"):
                breaked = 0
                continue

            if (result[0][0] == '*' and result == "*0-0" and breaks[0] > breaks[1]):
                breaked = 1
            elif (result == "0-0*" and breaks[1] > breaks[0]):
                breaked = 1
            elif (result == "0-0*" or result == "*0-0"):
                breaked = 0

            if (not (result == "*0-0" or result == "0-0*")):
                if (breaked > 0):
                    if (result2[0] != prev_result and result2[0][0] == '*'):
                        OSVOJENI[row['Home']][0] += 1
                        OSVOJENI[row['Home']][1] += 1
                    elif (result2[0][0] == '*'):
                        OSVOJENI[row['Home']][1] += 1
                    elif (result2[0] != prev_result):
                        IZGUBLJENI[row['Away']][1] += 1
                    else:
                        IZGUBLJENI[row['Away']][0] += 1
                        IZGUBLJENI[row['Away']][1] += 1
                elif (breaked < 0):
                    if (result2[0] != prev_result and result2[1][-1] == '*'):
                        OSVOJENI[row['Away']][1] += 1
                    elif (result2[1][-1] == '*'):
                        OSVOJENI[row['Away']][0] += 1
                        OSVOJENI[row['Away']][1] += 1
                    elif (result2[0] != prev_result):
                        IZGUBLJENI[row['Home']][0] += 1
                        IZGUBLJENI[row['Home']][1] += 1
                    else:
                        IZGUBLJENI[row['Home']][1] += 1

            prev_result = result2[0]


def izracunaj_vjerojatnosti():
    output = []

    for igrac in OSVOJENI.keys():
        osvojeni = -1
        izgubljeni = -1
        if (OSVOJENI[igrac][1] == 0):
            osvojeni = 0
        if (IZGUBLJENI[igrac][1] == 0):
            izgubljeni = 0
        
        if (osvojeni == -1):
            osvojeni = OSVOJENI[igrac][0] / OSVOJENI[igrac][1]
        if (izgubljeni == -1):
            izgubljeni = IZGUBLJENI[igrac][0] / IZGUBLJENI[igrac][1]
        output.append({"Player": igrac,
        "Win": osvojeni, "Lose": izgubljeni})

    return output


def upisi_u_novu_csv_datoteku(data):
    path = 'statistike/break_vjerojatnosti.csv'

    try:
        with open(path, 'w', encoding = 'ISO-8859-1') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Player", "Win", "Lose"])
            
            writer.writeheader()

            for row in data:
                writer.writerow(row)

    except IOError:
        print("I/O Error")

broji_osvojene_bodove("filtriraniIzbaceno/tenis_2015_sportevent_1.csv")
broji_osvojene_bodove("filtriraniIzbaceno/tenis_2015_sportevent_2.csv")
broji_osvojene_bodove("filtriraniIzbaceno/tenis_2015_sportevent_3.csv")
broji_osvojene_bodove("filtriraniIzbaceno/tenis_2016_01_sportevent.csv")
broji_osvojene_bodove("filtriraniIzbaceno/tenis_2016_02_sportevent.csv")
broji_osvojene_bodove("filtriraniIzbaceno/tenis_2016_03_sportevent.csv")
broji_osvojene_bodove("filtriraniIzbaceno/tenis_2016_04_sportevent.csv")
broji_osvojene_bodove("filtriraniIzbaceno/tenis_2016_05_sportevent.csv")

vjerojatnosti = izracunaj_vjerojatnosti()

upisi_u_novu_csv_datoteku(vjerojatnosti)