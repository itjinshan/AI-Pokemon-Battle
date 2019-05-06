import Pokemon
class Player:
    session = None
    log:str = ""
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory
    def getTurn(self): # this will return some move that will be applyed during play
        pass # it may also apply an internal adjustments, such as taking a pokemon out of battle
    def getCurrentPokemon(self):
        pass
    def initalizeGame(self, session):
        self.session = session
    def requestBackup(self): # this will return true or false depending on whether the player can continue
        pass
    def append_to_log(self, str):
        self.log += str

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
            self.swap_request()
            return None
        else:
            return self.currentPokemon.moveList[choice-1] # return the move we selected from our list

    def setCurrentPokemon(self, index):
        self.currentPokemon = self.inventory[index]

    def getCurrentPokemon(self):
        return self.currentPokemon

    def life_check(self)->bool:
        for pokemon in self.inventory:
            if not pokemon.is_dead():
                return False
        return True

    def swap_request(self):
        index = 1
        invalid_choice = True
        while invalid_choice:
            for pokemon in self.inventor:
                if not pokemon.is_dead():
                    print(str(index)+". "+pokemon.name)
                index += 1
            choice = input("Enter a number to select a pokemon:")
            selected_pok = self.inventory[choice-1]
            if not selected_pok.is_dead():
                invalid_choice = False
                self.setCurrentPokemon(choice-1)

    def requestBackup(self)->bool:
        if self.life_check():
            print("Your inventory is depleted")
            return False
        print("Your selected pokemon has fainted in battle, please select another: ")
        self.swap_request()
        return True

    def initalizeGame(self, session):
        super.initalizeGame(session)
        self.swap_request() # request our current pokemon


class GameSession:

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.log = ""
        self.lastCmd = ""
        self.winner = None

    def isGameOver(self)->bool:
        pass

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
