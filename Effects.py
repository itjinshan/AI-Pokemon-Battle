
def get_ailment(ailment):
    pass

class Effect:
    pass

class Paralysis(Effect): #speed reduced by 50% and 25% of skipping next turn
    pass

class Burn(Effect): #6% health reduction every turn, physical move damage reduced by 50%
    pass

class Frozen(Effect): # can't move until un-frozen, there is 20% of un thawing evey turn
    pass # fire moves do unfreeze this though.

class Poison_light(Effect): # 12.5% hp reduction every turn, doesn't wear off
    pass

class Poison_heavy(Effect): # 1/16*n, where n is the number of turns this effect has been applied, %hp reduction
    pass # every turn

class Sleep(Effect): # cannot move until effect subsides
    pass

# TODO: there are a few popular moves that have special status effects that need to be implemented, hard code these
# TODO: you can actually get healing information for certain moves like recover, check the meta section
# TODO: every EV is 85 and every IV is 31, you can use these along with the type to get a good estimate of actual base hp