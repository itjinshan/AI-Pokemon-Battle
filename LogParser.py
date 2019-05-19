import re

RE_F_DMG = r"(?:\()(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
RE_H_DMG = r"(?:\(The opposing )(?P<name>['a-zA-Z\-]+)(?: lost )(?P<number>[0-9]+(\.[0-9]+)?)(?:% of its health!\))"
RE_H_MOVE = r"(?:The opposing )(?P<name>['a-zA-Z\-]+)(?: used )(?P<move_name>['a-zA-Z\- ]+)(?:!)"
RE_H_EFFECT = r"(?:The opposing )(?P<name>['a-zA-Z\-]+)(?: was )(?P<effect_text>['a-zA-Z\- ]+)(?:!)"
RE_F_EFFECT = r"(?P<name>['a-zA-Z\-]+)(?: was )(?P<effect_text>['a-zA-Z\- ]+)(?:!)"
RE_H_SWAP = r"(?P<player>['a-zA-Z\- ]+(?:sent out ))"
class percept_struct:
    def __init__(self, h_move=None, f_effects=None, h_effects=None, f_stat_changes=None, h_stat_changes=None):
        self.h_move = h_move
        self.f_effects = f_effects
        self.h_effects = h_effects
        self.f_stat_changes = f_stat_changes
        self.h_stat_changes = h_stat_changes

