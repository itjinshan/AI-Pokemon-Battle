import Move
import Stats

name = ""
level = 0
currentHP = 0
ability = None
item = None
moveList = None
stats = None

def __init__(self, name, level, currentHP, ability, item, moveList, stats):
	this.name = name
	this.level = level
	this.currentHP = currentHP
	this.ability = ability
	this.item = item
	this.moveList = moveList
	this.stats = stats

def decreaseHP(value):
	this.currentHP -= value
	if currentHP < 0:
		# do something
