import random

# NOTE: Right now, we assume that effects will never be removed from the affected pokemon; they permanently modify stats


def get_ailment(ailment):
    pass


class Effect:
    def __init__(self):
        self.target = None
        self.stat_effects = {
            "sp_Attack":1.0,
            "sp_Defense":1.0,
            "Attack":1.0,
            "Defense":1.0,
            "Speed":1.0,
            "HP":1.0,
            "Damage_Output":1.0
        }

    def set_target(self, target):
        self.target = target

    def block_move(self)->bool:
        pass

    def update_effect(self):
        pass


class Paralysis(Effect):  # speed reduced by 50% and 25% of skipping next turn
    def __init__(self):
        super().__init__()
        self.stat_effects["Speed"] = 0.5 # we reduce the speed of the target by 50%

    def block_move(self)->bool:
        return random.randint(0, 100) <= 25


class Burn(Effect):  # 6% health reduction every turn, physical move damage reduced by 50%
    def __init__(self):
        super().__init__()
        self.stat_effects["Damage_Output"] = 0.5 # we'll assume all moves are physical

    def block_move(self):
        return False

    def update_effect(self):
        self.target.update_hp(percent=-6)

class Frozen(Effect): # can't move until un-frozen, there is 20% of un thawing evey turn, fire moves do unfreeze this though.
    def __init__(self):
        super().__init__()
        self.is_frozen = True

    def block_move(self):
        return self.is_frozen

    def update_effect(self):
        if self.is_frozen:
            if random.randint(0, 100) <= 20:  # can we un-thaw?
                self.is_frozen = False  # we're thawed out


class Poison_light(Effect): # 12.5% hp reduction every turn, doesn't wear off
    def __init__(self):
        super().__init__()

    def block_move(self):
        return False

    def update_effect(self):
        self.target.update_hp(percent=-12.5)


class Poison_heavy(Effect):  # 1/16*n, where n is the number of turns this effect has been applied, %hp reduction
    def __init__(self):
        super().__init__()
        self.counter = 0

    def block_move(self):
        return False

    def update_effect(self):
        self.counter += 1
        percent_reduction = (1/16)*self.counter
        self.target.update_hp(percent=-percent_reduction)


class Sleep(Effect):  # cannot move until effect subsides
    def __init__(self):
        super().__init__()

    def block_move(self):
        return True

    def update_effect(self):
        pass


# TODO: there are a few popular moves that have special status effects that need to be implemented, hard code these