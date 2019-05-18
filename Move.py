import requests
import random
import Effects
def get_move_from_api(ID:int=None, Name:str=None, URL:str=None) -> dict:
    url = ""
    if ID is not None:
        url = "https://pokeapi.co/api/v2/move/"+str(ID)+"/"
    elif Name is not None:
        url = "https://pokeapi.co/api/v2/move/"+Name+"/"
    elif URL is not None:
        url = URL
    else:
        return None
    try:
        url_d = requests.get(url)
        return url_d.json()
    except:
        print("Could not open url "+url)
        return None

class Move:
    def parse_data_from_string(self, p_str:str):
        pass
    def __init__(self, ParseString:str=None, ID:int=None, URL:str = None, Name:str = None):
        self.data_dict = get_move_from_api(ID=ID, Name=Name, URL=URL)
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

    def apply_effect(self, user, target)->Effects.Effect:
        translation_table = {"attack":"Attack", "defense":"Defense", "special-attack":"sp_Attack",
                             "special-defense":"sp_Defense", "speed":"Speed"}

        user.update_hp(percent=int(self.meta_data["healing"]))

        for entry in self.stat_change:
            if entry["stat"]["name"] in translation_table: # if it isn't in the translation table, ignore it
                if self.data_dict["target"]["name"] is "user":
                    user.update_stat_stage(translation_table[entry["stat"]["name"]], entry["change"])
                else:
                    target.update_stat_stage(translation_table[entry["stat"]["name"]], entry["change"])

        if ("ailment" in self.meta_data and
           self.data_dict["effect_chance"] is not None and
           random.randint(0, 100) <= int(self.data_dict["effect_chance"])):
            effect = Effects.get_ailment(self.meta_data["ailment"]["name"])
            if self.data_dict["target"]["name"] is "user":
                user.apply_effect(effect)
            else:
                target.apply_effect(effect)
            return effect
        return None



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


# TODO: there are a few popular moves that have special status effects that need to be implemented, hard code these
