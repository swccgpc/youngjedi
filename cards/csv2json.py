#!/usr/bin/env python3


import csv
import json
import os.path
from pathlib import Path

csv_files = {
  1: {"name":"menace of darth maul",          "abbr":"DM",  "csv":"menaceofdarthmaul/index.csv"},
  2: {"name":"the jedi council",              "abbr":"JC",  "csv":"thejedicouncil/index.csv"},
  3: {"name":"battle of naboo",               "abbr":"BN",  "csv":"battleofnaboo/index.csv"},
  4: {"name":"enhanced menace of darth maul", "abbr":"EDM", "csv":"enhancedmenaceofdarthmaul/index.csv"},
  5: {"name":"duel of the fates",             "abbr":"DF",  "csv":"duelofthefates/index.csv"},
  6: {"name":"enhanced battle of naboo",      "abbr":"EBN", "csv":"enhancedbattleofnaboo/index.csv"},
  7: {"name":"reflections",                   "abbr":"RF",  "csv":"reflections/index2.csv"},
  8: {"name":"boonta eve podrace",            "abbr":"BP",  "csv":"boontaevepodrace/index.csv"},
}



#Set Name Abbreviations: 
#MDM = Menace Of Darth Maul 
#TJC = The Jedi Council 
#BON = Battle of Naboo 
#EMDM = Enhanced Menace Of Darth Maul 
#DOTF = Duel Of The Fates 
#EBON = Enhanced Battle Of Naboo 
#BEP = Boonta Eve Podrace (special preview) 
#PREM = Premium (Shmi Skywalker card only).




cards = []
cards_dark = []
cards_light = []
sets = []

print_row = False
print("")
for i in csv_files:
  csv_file = csv_files[i]["csv"]
  print("")
  print("  * "+str(i)+":["+csv_file+"]")

  sets.append({
    "id":       i,
    "name":     csv_files[i]["name"],
    "gempName": csv_files[i]["name"],
    "abbr":     csv_files[i]["abbr"],
    "legacy":   "false"
  })

  with open(csv_file) as cf:
    rows = csv.reader(cf, delimiter='|')

    for row in rows:
      if (print_row):
        print(len(row), row)

      if (len(row) > 0):
        side     = row[1].strip()
        release  = row[2].strip().lower()
        cardtype = row[3].strip().lower()
        cardid   = row[4].strip()
        name     = row[5].strip()
        image    = row[6].strip()
        rarity   = row[7].strip().lower()
        subtype  = ""
        foil     = "false"

        if (cardid[0:1] == "F"):
          subtype = "foil"
          foil    = "true"

        #if (cardid == "F8"):
        #  print_row = True


        #print('"' + release + "\"\t\"" + cardtype + "\"\t\"" + cardid + "\"\t\"" + name + "\"\t\"" + image + "\"\t\"" + rarity + '"')
        print('    ** [' + cardid + "]:\t\"" + name + "\"")

        missing_images = [
          #"/menaceofdarthmaul/light/20naboosecurityguard.gif",
          #"/duelofthefates/dark/raynovaca.gif",
          #"/duelofthefates/light/yodajediphilosopher.gif",
          #"/duelofthefates/light/quigonnsfinalstand.gif",
          ]

        if (image in missing_images):
          image = "/missing_image.png"
        elif not os.path.isfile('.'+image):
          print('       *** Image missing: '+image)
          image_bits        = image.split("/")
          search_for_path  = image_bits[1] + "/" + image_bits[2]
          search_for_image = image_bits[3][0:8] + "*"
          print('       *** Searching in.: /'+search_for_path)
          print('       *** For image....: '+search_for_image)

          for found_image in Path(search_for_path).glob(search_for_image):
            print('       *** Found image..: /'+str(found_image))
          exit(1)
          #if not os.path.isfile('.'+image):
          #  print('       *** Image missing: .'+image)




        card = {
          "id": i,
          "gempId": str(i)+"_"+cardid,
          "side": side.capitalize(),
          "rarity": rarity,
          "set": i,
          "printings": [{"set": release}],
          "foil": foil,
          "front": {
            "title": name,
            "imageUrl": "https://res.starwarsccg.org/youngjedi/cards"+image,
            "type": cardtype,
            "subType": subtype,
            "destiny": "9999",
            "power": "9999",
            "deploy": "9999",
            "forfeit": "9999",
            "gametext": "xxxxxxxx",
            "lore": "yyyyyyyyy",
            "extraText": [""]
          },
          "counterpart": "",
          #"legacy": "false"
        }
        if (side == "dark"):
          cards_dark.append(card)
        else:
          cards_light.append(card)


print("")

fh = open("Dark.json", "w")
fh.write(json.dumps({"cards":cards_dark}, indent=2))
fh.close()

fh = open("Light.json", "w")
fh.write(json.dumps({"cards":cards_light}, indent=2))
fh.close()

fh = open("sets.json", "w")
fh.write(json.dumps(sets, indent=2))
fh.close()

print("cards written to: Dark.json and Light.json")
print("sets written to: sets.json")
print("")

