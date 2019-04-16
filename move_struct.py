class Move:
	name = ""
	basePower = 0
	moveType = ""
	accuracy = 0
	pp = 0
	attack = False
	spAttack = False

	def __init__(self, name, basePower, moveType, accuracy, pp, attack, spAttack):
		this.name = name
		this.basePower = basePower
		this.moveType = moveType
		this.accuracy = accuracy
		this.pp = pp
		this.attack = attack
		this.spAttack = spAttack

	def decrementPP(isPressure):
		if isPressure == false:
			this.pp -= 1
		else:
			this.pp -= 2