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
        # We save the data_dict so that we can easily access relent information about the pokemon in the future.
        # Next, we must initialize our pokemons stats, for the sake of simplicity, these will be stored as ints
        self.stat = {}
        # 0 - Speed, 1 - special defense, 2 - special-attack, 3 - defense, 4 - attack, 5 - HP
        self.stat["Attack"] = self.data_dict["stats"][4]["base_stat"]
        self.stat["Defense"] = self.data_dict["stats"][3]["base_stat"]
        self.stat["HP"] = self.data_dict["stats"][5]["base_stat"]
        self.stat["Speed"] = self.data_dict["stats"][0]["base_stat"]
        self.stat["sp_Defense"] = self.data_dict["stats"][1]["base_stat"]
        self.stat["sp_Attack"] = self.data_dict["stats"][2]["base_stat"]

        self.moves = list()

    def Damage(self, other, move):
        dmg = ( ( (2*other.lvl/5 + 2)*move.power*self.stat["Attack"]/other.stat["Defense"] )/50 + 2 ) * GLOBAL_MOD

a = Pokemon(1)
print("done.")