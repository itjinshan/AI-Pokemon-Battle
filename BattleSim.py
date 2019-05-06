import Pokemon
class Player:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory
    def getTurn(self): # this will return some move that will be applyed during play
        pass # it may also apply an internal adjustments, such as taking a pokemon out of battle
    def getCurrentPokemon(self):
        pass
    def initalizeGame(self):
        pass
    def requestBackup(self): # this will return true or false depending on whether the player can continue
        pass

class HumanPlayer(Player):
    def __init__(self, name, inventory):
        """

        :param name: Name of this player
        :param inventory: A list of all the pokemon the player drew from his deck

        The current pokemon will be selected as the first pokemon in the deck for now.
        """
        super(name, inventory)
        self.setCurrentPokemon(0)
    def getTurn(self):
        print("Possible Moves: ")
        index = 1
        for move in self.currentPokemon.moveList:
            print(str(index)+". "+move.name)
            index += 1
        swap_ind = index
        print(str(swap_ind)+". Swap the pokemon out:")
        choice = input("Enter a number to select a move:")
        if int(choice) == swap_ind:
            for pokemon in self.inventory:

    def setCurrentPokemon(self, index):
        self.currentPokemon = self.inventory[index]
    def getCurrentPokemon(self):
        return self.currentPokemon

class GameSession:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.winner = None
    def isGameOver(self)->bool:
        for pok in

    def getVictor(self):
        return self.winner

    def runGame(self):
        self.player1.initalizeGame()
        self.player2.initalizeGame()

        while self.isGameOver():
            if self.player1.getCurrentPokemon().is_dead():
                if not self.player1.requestBackup():  # if the opponent has no more pokemon to pull
                    self.winner = self.player2
                    return self.player2

            if self.player2.getCurrentPokemon().is_dead():
                if not self.player2.requestBackup():  # if the opponent has no more pokemon to pull
                    self.winner = self.player1
                    return self.player1

            move1 = self.player1.getTurn()
            move2 = self.player2.getTurn()

            if ((move1.priority > move2.priority) or
                (move1.priority == move2.priority and self.player1.stat["Speed"] > self.player2.stat["Speed"])):
                self.player1.getCurrentPokemon().do_damage(self.player2.getCurrentPokemon(), move1)
                if not self.player2.getCurrentPokemon().is_dead():
                    self.player2.getCurrentPokemon().do_damage(self.player1.getCurrentPokemon(), move2)
            else:
                self.player1.getCurrentPokemon().do_damage(self.player2.getCurrentPokemon(), move1)
                if not self.player2.getCurrentPokemon().is_dead():
                    self.player2.getCurrentPokemon().do_damage(self.player1.getCurrentPokemon(), move2)
