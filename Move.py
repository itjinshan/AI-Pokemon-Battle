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
        self.name = self.data_dict["name"]
        self.power = self.data_dict["power"]
        self.accuracy = self.data_dict["accuracy"]
        self.power_points = self.data_dict["pp"]
        self.type = self.data_dict["type"]["name"]
        self.priority = self.data_dict["priority"]
        self.meta_data = self.data_dict["meta"]

    def applyEffects(self, target):
        pass

d = Move(Name="flamethrower")
print(d.name)
print(d.accuracy)
print(d.power)
print(d.power_points)
print(d.type)
print(d.priority)

