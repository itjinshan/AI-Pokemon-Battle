import pokemon_struct
class Player:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory
    def getTurn(self): # this will return some move that will be applyed during play
        pass # it may also apply an internal adjustments, such as taking a pokemon out of battle
    def getCurrentPokemon(self):
        pass
    def requestBackup(self): # this will return true or false depending on whether the player can continue
        pass

class HumanPlayer(Player):
    def __init__(self, name, inventory):
        super(name, inventory)
    def getTurn(self):
        print("Possible Moves: ")


class GameSession:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
    def isGameOver(self)->bool:
        pass
    def runGame(self):

        player_table = [self.player1, self.player2]
        player_index = 0
        while not self.isGameOver():
            aggressor = player_table[player_index]
            defender = player_table[int(not player_index)]

            move = aggressor.getMove()
            defender.getCurrentPokemon().doDamage(move)
            #check to see if the other player's pokemon is dead
            if defender.getCurrentPokemon().isDead():
                #check to see if they have another pokemon they can put into play,
                #otherwise the game is over, and the aggressor wins
                if not defender.requestBackup():
                    print(aggressor.name+"is the Winner!")
                    return
        player_index = int(not player_index) # switch turns

