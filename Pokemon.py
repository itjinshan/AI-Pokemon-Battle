import requests
import random
import Effects
import csv
from Move import Move
from Move import Swap
from Move import Faint
GLOBAL_MOD = 1.0
MAX_MOVES_PER_POKEMON = 4
MAX_CHOOSEABLE_POKEMON = 807
PKM_IV = 31
PKM_EV = 85  # taken from the pokemon github repository
STAT_STAGE_COEFFICIENTS = {-6:2/8, -5:2/7, -4:2/6, -3:2/5, -2:2/4, -1:2/3, 0:2/2,
                           1:3/2, 2:4/2, 3:5/2, 4:6/2, 5:7/2, 6:8/2}  # taken from bulbapedia
def load_type_table():  # this will return a 2d list of values corresponding to each type
    ret_list = list()
    with open("type_csv.csv") as file:
        data = csv.reader(file, delimiter=',')  # we need the sig, otherwise we also get ï»¿
        return [[float(j) for j in row] for row in data]
        #return data

TYPE_MOD_TABLE = load_type_table()# https://bulbapedia.bulbagarden.net/wiki/Type, rows are attacking, columns are defending

TYPE_TRANSLATION_TABLE = {"normal":0,"fighting":1,
                  "flying":2,"poison":3,
                  "ground":4,"rock":5,
                  "bug":6,"ghost":7,
                  "steel":8,"fire":9,
                  "water":10,"grass":11,
                  "electric":12,"psychic":13,
                  "ice":14,"dragon":15,
                  "dark":16,"fairy":17}


def get_pokemon_from_api(ID:int=None, Name:str=None, URL:str = None) -> dict:
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
    def parse_data_from_string(self, p_str: str):
        '''

        :param p_str: the parsable string, see info below
        :return: None
        This function is designed to take a parsable string of the form:
        [<PokemonName>, L<lvl #>]
        HP: <HP percent>% (<current hp>/<max hp>)
        Ability: <Ability> / Item: <Item>
        Atk <stat> / Def <stat> / SpA <stat> / SpD <stat> / Spe <stat>
        • <Move>
        • <Move>
        • <Move>
        • <Move>
        for example:

        [u'Solgaleo', u'L78']
        HP: 100.0% (342/342)
        Ability: Full Metal Body / Item: Leftovers
        Atk 259 / Def 212 / SpA 221 / SpD 184 / Spe 196
        • Zen Headbutt
        • Sunsteel Strike
        • Flare Blitz
        • Morning Sun
        ...
        '''
        lines = p_str.splitlines()
        tokens = lines[0].replace("u'", "").replace("'", "").replace("[","").replace("]","").split(", ")
        self.data_dict = get_pokemon_from_api(Name=tokens[0].lower())
        self.name = tokens[0].lower()
        self.lvl = int(tokens[1].replace("L", ""))
        tokens = lines[1].split(" ")
        hpLine = tokens[2].replace("(", "").replace(")", "").split("/")
        self.HP = int(hpLine[0])
        self.stat["HP"] = int(hpLine[1])
        # right now, we don't do anything with abilities or items, as there is no efficient way to get info about them
        tokens = lines[3].split(" / ")
        self.stat["Attack"] = int(tokens[0].split(" ")[1])
        self.stat["Defense"] = int(tokens[1].split(" ")[1])
        self.stat["sp_Attack"] = int(tokens[2].split(" ")[1])
        self.stat["sp_Defense"] = int(tokens[3].split(" ")[1])
        self.stat["Speed"] = int(tokens[4].split(" ")[1])
        self.type = self.data_dict["types"][0]["type"]["name"]
        for s in lines[4:]:
            self.add_move(Name=s.replace("• ", "").lower().replace(" ", "-"))

    def __init__(self, ParseString:str=None, ID:int = None, Name:str=None):
        """

        :param parseString: A parsable string containing the information about this pokemon.

        """
        self.moveList = list()
        self.effect_list = list()
        self.stat = {"HP":0, "Attack":0, "Defense":0, "sp_Attack":0, "sp_Defense":0, "Speed":0}
        self.stat_stages = dict((key, 0) for key in self.stat.keys())
        if ParseString is not None:
            self.parse_data_from_string(p_str=ParseString)
            return
        if ID is not None:
            self.data_dict = get_pokemon_from_api(ID=ID)
        elif Name is not None:
            self.data_dict = get_pokemon_from_api(Name=Name)
        self.lvl = 1
        self.name = self.data_dict["name"]
        self.calculate_stats(1)
        self.HP = int(self.get_stat("HP"))
        self.type = self.data_dict["types"][0]["type"]["name"]

    def get_effect_stat(self, stat):
        stat_coef = 1.0
        for effect in self.effect_list:
            stat_coef *= effect.stat_effects[stat]
        return stat_coef

    def can_play(self)->bool:
        for effect in self.effect_list:
            if effect.block_move():
                return False
        return True

    def add_move(self, ParseString:str=None, ID:int=None, Name:str=None, URL:str=None):
        self.moveList.append(Move(ParseString=ParseString, Name=Name, ID=ID, URL=URL))

    def get_stat(self, stat):
        return self.stat[stat]*STAT_STAGE_COEFFICIENTS[self.stat_stages[stat]]*self.get_effect_stat(stat)

    def update_stat_stage(self, stat, value):
        self.stat_stages[stat] += value
        self.stat_stages[stat] = min(max(self.stat_stages[stat], -6), 6)  # clamp the value between 6 and -6

    def reset_stat_stage(self):
        self.stat_stages = dict((key, 0) for key in self.stat.keys())

    def apply_damage(self, other, move)->(float, Move, Effects.Effect):
        # the modifier would be something this:
        #

        if (move is None
           or isinstance(move, Swap)
           or isinstance(move, Faint)
           or not self.can_play()):
            return (0.0, move, None)

        effect = move.apply_effect(self, other)  # we do any heal or w/e at this point
        dmg = 0.0

        if move.power is not None:  # formula provided by Bulbapedia
            mod = (TYPE_MOD_TABLE[TYPE_TRANSLATION_TABLE[self.type]][TYPE_TRANSLATION_TABLE[other.type]]
                   * (1.5 if move.type == self.type else 1.0))  # Type * STAB
            if move.is_special:
                dmg = (((2 * self.lvl / 5 + 2) * move.power * self.get_stat("sp_Attack")
                        / other.get_stat("sp_Defense")) / 50 + 2) * GLOBAL_MOD * self.get_effect_stat("Damage_Output")
            else:
                dmg = (((2*self.lvl/5 + 2) * move.power * self.get_stat("Attack")
                        / other.get_stat("Defense")) / 50 + 2) * GLOBAL_MOD * self.get_effect_stat("Damage_Output")
            dmg *= mod

        other.HP -= dmg
        return ((dmg/other.get_stat("HP"))*100, move, effect)

    def apply_effect(self, effect=None):
        if effect is not None:
            effect.target(self)
            self.effect_list.append(effect)
        for effect in self.effect_list:
            effect.update_effect()

    def update_hp(self, percent=None, points=None):
        if points is not None:
            self.HP += points
            self.HP = min(self.HP, self.get_stat("HP"))
        elif percent is not None:
            points = self.get_stat("HP")*(percent/100)
            self.HP = min(self.HP+points, self.get_stat("HP"))
        else:
            pass

    def calculate_stats(self, nature_mod):
        def hp_calc(base, lvl):
            frac_perc = ((2*base+PKM_IV+(PKM_EV/4))*lvl)/100
            return int(frac_perc+lvl+10)

        def stat_calc(base, lvl, nature_mod):
            frac_perc = (((2 * base + PKM_IV + (PKM_EV / 4)) * lvl) / 100) + 5
            return int(frac_perc * nature_mod)

        # 0 - Speed, 1 - special defense, 2 - special-attack, 3 - defense, 4 - attack, 5 - HP
        base_speed = int(self.data_dict["stats"][0]["base_stat"])
        base_sp_defense = int(self.data_dict["stats"][1]["base_stat"])
        base_sp_attack = int(self.data_dict["stats"][2]["base_stat"])
        base_defense = int(self.data_dict["stats"][3]["base_stat"])
        base_attack = int(self.data_dict["stats"][4]["base_stat"])
        base_hp = int(self.data_dict["stats"][5]["base_stat"])

        self.stat["Attack"] = stat_calc(base_attack, self.lvl, 1)
        self.stat["Defense"] = stat_calc(base_defense, self.lvl, 1)
        self.stat["HP"] = hp_calc(base_hp, self.lvl)
        self.stat["Speed"] = stat_calc(base_speed, self.lvl, 1)
        self.stat["sp_Defense"] = stat_calc(base_sp_defense, self.lvl, 1)
        self.stat["sp_Attack"] = stat_calc(base_sp_attack, self.lvl, 1)
        self.HP = self.stat["HP"]

    def is_dead(self):
        return self.HP <= 0

    def get_info_str(self):
        r_str = "[u'"+self.name+"', u'L"+str(self.lvl)+"']\n"
        r_str +="HP: "+str((self.HP/self.stat["HP"])*100)+"% ("+str(self.HP)+"/"+str(self.stat["HP"])+")\n"
        r_str +="Ability:\n"
        r_str +=("Atk "+str(self.stat["Attack"])+" / Def "+str(self.stat["Defense"]) +
                 " / SpA "+str(self.stat["sp_Attack"])+" / SpD "+str(self.stat["sp_Defense"]) +
                 " / Spe "+str(self.stat["Speed"])+"\n")
        for move in self.moveList:
            r_str+= "• "+move.name+"\n"
        return r_str


def assign_random_moves(pokemon):
    possible_move_list = pokemon.data_dict["moves"]
    for i in range(min(MAX_MOVES_PER_POKEMON, len(possible_move_list))):
        move = random.choice(possible_move_list)
        pokemon.add_move(URL=move["move"]["url"])


def get_random_pokemon() -> Pokemon:
    n_poke = Pokemon(ID=random.randint(1, MAX_CHOOSEABLE_POKEMON))
    assign_random_moves(n_poke)
    n_poke.lvl = random.randint(1, 100)
    n_poke.calculate_stats(1)
    return n_poke
'''
poke = getRandomPokemon()
print(poke.get_info_str())
print("done.")
'''
'''
p_str = ("[u'Solgaleo', u'L78']\nHP: 100.0% (342/342)\n"
         "Ability: Full Metal Body / Item: Leftovers\n"
         "Atk 259 / Def 212 / SpA 221 / SpD 184 / Spe 196\n"
         "• Zen Headbutt\n"
         "• Sunsteel Strike\n"
         "• Flare Blitz\n"
         "• Morning Sun")
poke = Pokemon(ParseString=p_str)
print(poke.get_info_str())
'''