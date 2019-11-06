import requests
from bs4 import BeautifulSoup
from random import randint

src = requests.get("https://pokemondb.net/pokedex/all").content

db = BeautifulSoup(src, 'lxml')

team = []

myTeam = []
inTeam = []


def isCorrect(myTeamDone):
    if len(myTeamDone) is not 6:
        return False
    typesInTeam = []
    for pkemon in myTeamDone:
        if pkemon[1] not in typesInTeam:
            typesInTeam.append(pkemon[1])
        if pkemon[2] not in typesInTeam:
            typesInTeam.append(pkemon[2])
    if len(typesInTeam) is not 12:
        return False
    return True
    pass


for i in range(6):
    team.append(randint(1, 809))

while not isCorrect(myTeam):

    data = db.find("tbody")

    toFind = 6 - len(myTeam)

    for _ in range(toFind):
        team.append(randint(1, 809))

    for tr in data.find_all("tr"):
        nametag = tr.find("td")
        pokeid = nametag.find_all("span")[2]
        if int(pokeid.text) in team:
            myPokemon = []
            inTeam.append(tr)
            nametag = tr.find_all("td")[1]
            name = nametag.find('a').text
            myPokemon.append(name)
            nametag = tr.find_all("td")[2]
            a_types = nametag.find_all("a")
            for a in a_types:
                myPokemon.append(a.text)
            myPokemon.append(int(pokeid.text))
            team.remove(int(pokeid.text))
            if len(myTeam) < 6:
                myTeam.append(myPokemon)

    i = len(myTeam) - 1
    while i >= 0:
        if len(myTeam[i]) < 4:
            myTeam.remove(myTeam[i])
            inTeam.pop(i)
        i -= 1

    i = len(myTeam) - 1
    types = []
    while i >= 0:
        pkmn = myTeam[i]
        if pkmn[1] not in types and pkmn[2] not in types:
            types.append(pkmn[1])
            types.append(pkmn[2])
        else:
            myTeam.remove(myTeam[i])
            inTeam.pop(i)
        i -= 1

    evolutions = []

    for poke in myTeam:
        if poke[0] not in evolutions:
            web = "https://pokemondb.net/pokedex/" + poke[0]
            evocrawl = requests.get(web).content
            evodb = BeautifulSoup(evocrawl, 'lxml')
            for dib in evodb.find_all("div", {"class": "infocard-list-evo"}):
                for span in dib.find_all("span", {"class": "infocard-lg-data text-muted"}):
                    nameofevotag = span.find("a")
                    nameofevo = nameofevotag.text
                    if nameofevo != poke[0]:
                        evolutions.append(nameofevo)

    i = len(myTeam) - 1
    while i >= 0:
        poke = myTeam[i]
        if poke[0] in evolutions:
            myTeam.remove(myTeam[i])
            inTeam.pop(i)
        i -= 1

    print("Current team consists of " + str(len(myTeam)) + " pokemons")

print("Final team: ")
print(myTeam)

print("Creating html file")
f = open("result.html", "w")
headers = "<h1>Equip Pokemon</h1><h2>HackEps 2019 - Galahad_3x</h2><table><tbody>"
f.write(headers)
f.write("<tr><td>Sprite</td><td>Nom</td><td>Tipus 1</td><td>Tipus 2</td><td>Número Pokédex</td></tr>")

for pokemon in myTeam:
    f.write("<tr><td>")
    data = db.find("tbody")
    for tr in data.find_all("tr"):
        nametag = tr.find("td")
        pokeid = nametag.find_all("span")[2]
        if int(pokeid.text) in pokemon:
            spritetag = nametag.find_all("span")[1]
            sprite = spritetag["data-src"]
            q = "\""
            f.write("<img src=" + q + str(sprite) + q + " alt=" + q + pokemon[
                0] + q + " width=" + q + "80" + q + " height=" + q + "60" + q + " />")
    f.write("</td>")
    for atr in pokemon:
        f.write("<td>" + str(atr) + "</td>")
    f.write("</tr>")

f.write("</tbody><table>")

print("Team creation complete. Please open file result.html")
