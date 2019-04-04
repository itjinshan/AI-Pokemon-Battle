import requests
import json
GLOBAL_MOD = 1.0
def getPokemonFromAPI(ID:int) -> dict:
    url = "https://pokeapi.co/api/v2/pokemon/"+str(ID)+"/"
    url_d = requests.get(url)
    return url_d.json()
class Pokemon:
    def __init__(self, ID):
        self.data_dict = getPokemonFromAPI(ID)
    def Damage(self, other, move):
        dmg = ( ( (2*other.lvl/5 + 2)*move.power*self.stat["Attack"]/other.stat["Defense"] )/50 + 2 ) * GLOBAL_MOD

a = Pokemon(1)
print("done.")