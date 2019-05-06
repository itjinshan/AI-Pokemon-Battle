import Move
from stat_struct import Stat
class pokemon_struct:
	name = ""
	level = 0
	currentHP = 0
	ability = None
	item = None
	moveList = None
	stats = None

	def __init__(self, name, level, currentHP, ability, item, moveList, stats):
		self.name = name
		self.level = level
		self.currentHP = currentHP
		self.ability = ability
		self.item = item
		self.moveList = moveList
		self.stats = stats

	def decreaseHP(self, value):
		self.currentHP -= value
		if self.currentHP < 0:
			pass # do something
