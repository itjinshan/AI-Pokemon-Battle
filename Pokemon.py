import requests
from Move import Move
GLOBAL_MOD = 1.0
def getPokemonFromAPI(ID:int=None, Name:str=None, URL:str = None) -> dict:
    url = ""
    if ID is not None:
        url = "https://pokeapi.co/api/v2/pokemon/"+str(ID)+"/"
    elif Name is not None:
        url = "https://pokeapi.co/api/v2/pokemon/"+Name+"/"
    elif URL is not None:
        url = URL
    else:
        return None
    url_d = requests.get(url)
    return url_d.json()

class Pokemon:
    def __init__(self, ID):
        self.data_dict = getPokemonFromAPI(ID)
        # We save the data_dict so that we can easily access relent information about the pokemon in the future.
        # Next, we must initialize our pokemon's stats, for the sake of simplicity, these will be stored as ints
        self.stat = {}
        # 0 - Speed, 1 - special defense, 2 - special-attack, 3 - defense, 4 - attack, 5 - HP
        self.stat["Attack"] = self.data_dict["stats"][4]["base_stat"]
        self.stat["Defense"] = self.data_dict["stats"][3]["base_stat"]
        self.stat["HP"] = self.data_dict["stats"][5]["base_stat"]
        self.stat["Speed"] = self.data_dict["stats"][0]["base_stat"]
        self.stat["sp_Defense"] = self.data_dict["stats"][1]["base_stat"]
        self.stat["sp_Attack"] = self.data_dict["stats"][2]["base_stat"]
        self.HP = self.stat["HP"]  # We initialize our running health with the base hp stat
        self.moves = list()
        for x in self.data_dict["moves"]:
            self.moves.append(Move(x["move"]["url"]))
    def Damage(self, other, move):
        dmg = (((2*self.lvl/5 + 2)*move.power*self.stat["Attack"]/other.stat["Defense"])/50 + 2) * GLOBAL_MOD
        other.HP -= dmg

a = Pokemon(1)
print("done.")