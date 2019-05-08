import requests
import random
from Move import Move
GLOBAL_MOD = 1.0
MAX_MOVES_PER_POKEMON = 4
MAX_CHOOSEABLE_POKEMON = 807
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
    def parse_data_from_string(self, p_str:str):
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
        self.data_dict = getPokemonFromAPI(Name=tokens[0].lower())
        self.name = tokens[0].lower()
        self.lvl = int(tokens[1].replace("L", ""))
        tokens = lines[1].split(" ")
        hpLine = tokens[2].replace("(", "").replace(")", "").split("/")
        self.HP = int(hpLine[0])
        self.stat["HP"] = int(hpLine[1])
        #right now, we don't do anything with abilities or items, as there is no efficient way to get info about them
        tokens = lines[3].split(" / ")
        self.stat["Attack"] = int(tokens[0].split(" ")[1])
        self.stat["Defense"] = int(tokens[1].split(" ")[1])
        self.stat["sp_Attack"] = int(tokens[2].split(" ")[1])
        self.stat["sp_Defense"] = int(tokens[3].split(" ")[1])
        self.stat["Speed"] = int(tokens[4].split(" ")[1])
        for s in lines[4:]:
            self.add_move(Name=s.replace("• ", "").lower().replace(" ", "-"))

    def __init__(self, ParseString:str=None, ID:int = None, Name:str=None):
        """

        :param parseString: A parsable string containing the information about this pokemon.

        """
        if ParseString is not None:
            self.parse_data_from_string(p_str=ParseString)
            self.moveList = list()
            return
        if ID is not None:
            self.data_dict = getPokemonFromAPI(ID=ID)
        elif Name is not None:
            self.data_dict = getPokemonFromAPI(Name=Name)
        self.lvl = 0
        self.name = self.data_dict["name"]
        # We save the data_dict so that we can easily access relent information about the pokemon in the future.
        # Next, we must initialize our pokemon's stats, for the sake of simplicity, these will be stored as ints
        self.stat = {}
        # 0 - Speed, 1 - special defense, 2 - special-attack, 3 - defense, 4 - attack, 5 - HP
        self.stat["Attack"] = int(self.data_dict["stats"][4]["base_stat"])
        self.stat["Defense"] = int(self.data_dict["stats"][3]["base_stat"])
        self.stat["HP"] = int(self.data_dict["stats"][5]["base_stat"])
        self.stat["Speed"] = int(self.data_dict["stats"][0]["base_stat"])
        self.stat["sp_Defense"] = int(self.data_dict["stats"][1]["base_stat"])
        self.stat["sp_Attack"] = int(self.data_dict["stats"][2]["base_stat"])
        self.HP = int(self.stat["HP"])  # We initialize our running health with the base hp stat
        self.moveList = list()
        '''
        for x in self.data_dict["moves"]: # right now, we pull all possible learned moves from the api
            if x["version_group_details"][0]["level_learned_at"] <= self.lvl:
                self.moveList.append(Move(URL=x["move"]["url"]))'''

    def add_move(self, ParseString:str=None, ID:int=None, Name:str=None, URL:str=None):
        self.moveList.append(Move(ParseString=ParseString, Name=Name, ID=ID, URL=URL))

    def do_damage(self, other, move)->float:
        # the modifier would be something this:
        #
        if move is None:
            return 0.0
        move.applyEffects(other)
        dmg = (((2*self.lvl/5 + 2)*move.power*self.stat["Attack"]/other.stat["Defense"])/50 + 2) * GLOBAL_MOD
        other.HP -= dmg
        return (dmg/other.stat["HP"])*100

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

def assignRandomMoves(pokemon):
    possible_move_list = pokemon.data_dict["moves"]
    for i in range(min(MAX_MOVES_PER_POKEMON, len(possible_move_list))):
        move = random.choice(possible_move_list)
        pokemon.add_move(URL=move["move"]["url"])

def getRandomPokemon() -> Pokemon:
    n_poke = Pokemon(ID=random.randint(1, MAX_CHOOSEABLE_POKEMON))
    assignRandomMoves(n_poke)
    return n_poke

poke = getRandomPokemon()
print(poke.get_info_str())
print("done.")