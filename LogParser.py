import re
import Move
import Effects


class PerceptStruct:
    def __init__(self, h_move=None, f_effects=list(), h_effects=list(), f_stat_changes:dict=dict(), h_stat_changes:dict=dict(), h_swap=None):
        self.h_move = h_move
        self.f_effects = f_effects
        self.h_effects = h_effects
        self.f_stat_changes = f_stat_changes
        self.h_stat_changes = h_stat_changes
        self.h_swap = h_swap
        self.enemy_faint = False
        self.friendly_faint = False


class ParseItem:
    def __init__(self):
        self.parse_dict = dict()
        self.regex_str = None

    def attempt_parse(self, p_str:str)->bool:
        attempt = re.match(self.regex_str, p_str)
        if attempt is not None:
            self.parse_dict = attempt.groupdict()
            return True
        return False

    def modify_percept(self, percept: PerceptStruct):
        pass

def get_effect_from_text(p_str:str)->Effects.Effect:
    pass

class RE_H_DMG(ParseItem):
    def __init__(self):
        super().__init__()
        self.regex_str = r"(?:\(The opposing )(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
    def modify_percept(self, percept: PerceptStruct):
        if "HP_PERC" in percept.h_stat_changes.keys():
            percept.h_stat_changes["HP_PERC"] -= float(self.parse_dict["number"])
        else:
            percept.h_stat_changes["HP_PERC"] = -float(self.parse_dict["number"])


class RE_F_DMG(ParseItem):
    def __init__(self):
        super().__init__()
        self.regex_str = r"(?:\()(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
    def modify_percept(self, percept: PerceptStruct):
        if "HP_PERC" in percept.h_stat_changes.keys():
            percept.f_stat_changes["HP_PERC"] -= float(self.parse_dict["number"])
        else:
            percept.f_stat_changes["HP_PERC"] = -float(self.parse_dict["number"])


class RE_H_MOVE(ParseItem):
    def __init__(self):
        super().__init__()
        self.regex_str = r"(?:The opposing )(?P<name>['a-zA-Z\-]+)(?: used )(?P<move_name>['a-zA-Z\- ]+)(?:!)"
    def modify_percept(self, percept: PerceptStruct):
        percept.h_move = Move.Move(Name=self.parse_dict["move_name"].lower().replace(" ", "-"))


class RE_H_EFFECT(ParseItem):
    def __init__(self):
        super().__init__()
        self.regex_str = r"(?:The opposing )(?P<name>['a-zA-Z\-]+)(?:( was )|( is ))(?P<effect_text>['a-zA-Z\- ]+)(?:!.*)"
    def modify_percept(self, percept: PerceptStruct):
        effect = get_effect_from_text(self.parse_dict["effect_text"])
        if effect is not None:
            percept.h_effects.append(effect)


class RE_F_EFFECT(ParseItem):
    def __init__(self):
        super().__init__()
        self.regex_str = r"(?P<name>['a-zA-Z\-]+)(?:( was )|( is ))(?P<effect_text>['a-zA-Z\- ]+)(?:!.*)"
    def modify_percept(self, percept: PerceptStruct):
        effect = get_effect_from_text(self.parse_dict["effect_text"])
        if effect is not None:
            percept.f_effects.append(effect)

class RE_SWAP(ParseItem):
    def __init__(self):
        super().__init__()
        self.regex_str = r"(?P<player>['a-zA-Z0-9\- ]+)(?: sent out )(?P<name>['a-zA-Z\-]+)(?:!)"
    def modify_percept(self, percept: PerceptStruct):
        percept.h_swap = Move.Swap(None, self.parse_dict["name"])  # WARNING: I AM USING A STRING IN PLACE OF A POKEMON
class RE_FAINT(ParseItem):
    def __init__(self):
        super().__init__()
        self.regex_str = r"(?P<player>['a-zA-Z0-9\- ]+)(?: sent out )(?P<name>['a-zA-Z\-]+)(?:!)"
    def modify_percept(self, percept: PerceptStruct):
        percept.h_swap = Move.Swap(None, self.parse_dict["name"])  # WARNING: I AM USING A STRING IN PLACE OF A POKEMON
PARSER_LIST = [RE_H_DMG(),RE_F_DMG(),RE_H_MOVE(),RE_H_EFFECT(),RE_F_EFFECT(),RE_SWAP()]

#RE_H_DMG = r"(?:\(The opposing )(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
#RE_F_DMG = r"(?:\()(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
#RE_H_MOVE = r"(?:The opposing )(?P<name>['a-zA-Z\-]+)(?: used )(?P<move_name>['a-zA-Z\- ]+)(?:!)"
#RE_H_EFFECT = r"(?:The opposing )(?P<name>['a-zA-Z\-]+)(?:( was )|( is ))(?P<effect_text>['a-zA-Z\- ]+)(?:!.*)"
#RE_F_EFFECT = r"(?P<name>['a-zA-Z\-]+)(?:( was )|( is ))(?P<effect_text>['a-zA-Z\- ]+)(?:!.*)"
#RE_SWAP1 = r"(?P<player>['a-zA-Z0-9\- ]+)(?: sent out )(?P<name>['a-zA-Z\-]+)(?:!)"
#RE_SWAP2 = r"(?P<player>['a-zA-Z0-9\- ]+)(?: withdrew )(?P<name>['a-zA-Z\-]+)(?:!)"


def parse_log_data(parse_string:str) -> PerceptStruct:
    percept = PerceptStruct()
    for line in parse_string.splitlines():
        for parser in PARSER_LIST:
            if parser.attempt_parse(line):
                parser.modify_percept(percept)
                break
    return percept
