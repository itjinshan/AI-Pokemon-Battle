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
    def __init__(self, URL):
        self.data_dict = getMoveFromAPI(URL=URL)
        self.power = self.data_dict["power"]
        self.accuracy = self.data_dict["accuracy"]
        self.power_points = self.data_dict["pp"]
