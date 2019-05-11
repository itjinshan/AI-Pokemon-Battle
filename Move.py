import requests
def getMoveFromAPI(ID:int=None, Name:str=None, URL:str=None) -> dict:
    url = ""
    if ID is not None:
        url = "https://pokeapi.co/api/v2/move/"+str(ID)+"/"
    elif Name is not None:
        url = "https://pokeapi.co/api/v2/move/"+Name+"/"
    elif URL is not None:
        url = URL
    else:
        return None
    url_d = requests.get(url)
    return url_d.json()

class Move:
    def parse_data_from_string(self, p_str:str):
        pass
    def __init__(self, ParseString:str=None, ID:int=None, URL:str = None, Name:str = None):
        self.data_dict = getMoveFromAPI(ID=ID, Name=Name, URL=URL)
        if self.data_dict is not None:
            self.name = self.data_dict["name"]
            self.power = self.data_dict["power"]
            self.accuracy = self.data_dict["accuracy"]
            self.power_points = self.data_dict["pp"]
            self.type = self.data_dict["type"]["name"]
            self.priority = self.data_dict["priority"]
            self.meta_data = self.data_dict["meta"]
            self.is_special = self.data_dict["damage_class"]["name"] == "special"
            self.stat_change = self.data_dict["stat_changes"]

    def apply_effect(self, target):
        pass


class Swap(Move):
    def __init__(self, swaped_out, swaped_in):
        self.priority = 999
        self.swaped_out = swaped_out
        self.swaped_in = swaped_in


class Faint(Move):
    def __init__(self, pokemon):
        self.pokemon = pokemon

'''
d = Move(Name="flamethrower")
print(d.name)
print(d.accuracy)
print(d.power)
print(d.power_points)
print(d.type)
print(d.priority)
'''