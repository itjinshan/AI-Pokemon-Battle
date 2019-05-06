class Move:
	name = ""
	basePower = 0
	moveType = ""
	accuracy = 0
	pp = 0
	attack = False
	spAttack = False

	def __init__(self, name, basePower, moveType, accuracy, pp, attack, spAttack):
		self.name = name
		self.basePower = basePower
		self.moveType = moveType
		self.accuracy = accuracy
		self.pp = pp
		self.attack = attack
		self.spAttack = spAttack

	def decrementPP(self, isPressure):
		if isPressure == False:
			self.pp -= 1
		else:
			self.pp -= 2