import requests
import json
def getPokemonFromAPI(ID:int) -> dict:
    url = "https://pokeapi.co/api/v2/pokemon/"+str(ID)+"/"
    url_d = requests.get(url)
    return url_d.json()
class Pokemon:
    def __init__(self, ID):
        self.data_dict = getPokemonFromAPI(ID)

a = Pokemon(1)
print("done.")