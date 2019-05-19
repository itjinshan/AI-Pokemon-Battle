import re


class PerceptStruct:
    def __init__(self, h_move=None, f_effects=list(), h_effects=list(), f_stat_changes:dict=dict(), h_stat_changes:dict=dict()):
        self.h_move = h_move
        self.f_effects = f_effects
        self.h_effects = h_effects
        self.f_stat_changes = f_stat_changes
        self.h_stat_changes = h_stat_changes


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
class RE_H_DMG(ParseItem):
    def __init__(self):
        super().__init__()
        self.regex_str = r"(?:\(The opposing )(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
    def modify_percept(self, percept: PerceptStruct):
        if "HP_PERC" in percept.h_stat_changes.keys():
            percept.h_stat_changes["HP_PERC"] -= float(self.parse_dict["number"])
        else:
            percept.h_stat_changes["HP_PERC"] = -float(self.parse_dict["number"])

RE_H_DMG = r"(?:\(The opposing )(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
RE_F_DMG = r"(?:\()(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
RE_H_MOVE = r"(?:The opposing )(?P<name>['a-zA-Z\-]+)(?: used )(?P<move_name>['a-zA-Z\- ]+)(?:!)"
RE_H_EFFECT = r"(?:The opposing )(?P<name>['a-zA-Z\-]+)(?: was )(?P<effect_text>['a-zA-Z\- ]+)(?:!)"
RE_F_EFFECT = r"(?P<name>['a-zA-Z\-]+)(?: was )(?P<effect_text>['a-zA-Z\- ]+)(?:!)"
RE_SWAP1 = r"(?P<player>['a-zA-Z0-9\- ]+)(?: sent out )(?P<name>['a-zA-Z\-]+)(?:!)"
RE_SWAP2 = r"(?P<player>['a-zA-Z0-9\- ]+)(?: withdrew )(?P<name>['a-zA-Z\-]+)(?:!)"


def parse_log_data(parse_string:str) -> PerceptStruct:
    for line in parse_string.splitlines():
