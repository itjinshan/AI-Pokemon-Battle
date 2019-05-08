import Pokemon
import Move

'''
Different Types of log statements:

Deployment:
Go! <pokemon>!
<player name> sent out <new pokemon>
Withdrawl:
<player name> withdrew <pokemon>
Death:
<pokemon> fainted!

<pokemon> used <move name>!
The opposing <name of other player's pokemon> used <move name>!
OPTIONAL: It's super effective!

(<our pokemon's name> lost <base hp % loss>% of its health!)
(The opposing <pokemon name> lost <base hp % loss>% of its health!)

Misc:


'''

class Player:
    session = None
    log:str = ""
    opponent = None
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory
    def getTurn(self): # this will return some move that will be applyed during play
        pass # it may also apply an internal adjustments, such as taking a pokemon out of battle
    def getCurrentPokemon(self):
        pass
    def initalizeGame(self, session):
        self.session = session
        if self.session.player1 is self:
            self.opponent = self.session.player2
        else:
            self.opponent = self.session.player1
    def requestBackup(self): # this will return true or false depending on whether the player can continue
        pass
    def append_to_log(self, str):
        self.log += str
    def swap_request(self)->Move.Swap:
        pass

class HumanPlayer(Player):
    def __init__(self, name, inventory):
        """

        :param name: Name of this player
        :param inventory: A list of all the pokemon the player drew from his deck

        The current pokemon will be selected as the first pokemon in the deck for now.
        """
        super(name, inventory)
        self.currentPokemon = None

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
            return self.swap_request()
        else:
            return self.currentPokemon.moveList[choice-1] # return the move we selected from our list

    def setCurrentPokemon(self, index):
        self.currentPokemon = self.inventory[index]

    def getCurrentPokemon(self)->Pokemon.Pokemon:
        return self.currentPokemon

    def life_check(self)->bool:
        for pokemon in self.inventory:
            if not pokemon.is_dead():
                return False
        return True

    def swap_request(self)->Move.Swap:
        old_pokemon = self.currentPokemon
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
        return Move.Swap(old_pokemon, self.currentPokemon)

    def requestBackup(self)->bool:
        if self.life_check():
            print("Your inventory is depleted")
            return False
        print("Your selected pokemon has fainted in battle, please select another: ")
        self.swap_request()
        return True

    def initalizeGame(self, session):
        super.initalizeGame(session)
        return self.swap_request() # request our current pokemon

class RandomPlayer(Player):
    pass


class GameSession:
    def get_move_string(self, attacker, move, is_friendly)->str:
        r_str = ""
        if is_friendly: # we are the attacker
            if isinstance(move, Move.Swap): # we just swapped something out
                #r_str += attacker.name+" withdrew "+move.swaped_out+"\n"
                r_str += "Go! "+move.swaped_in+"!\n"
            elif isinstance(move, Move.Faint): # i've got bad news
                r_str += move.pokemon.name + " fainted!\n"
            else: # we've attacked our target
                r_str += attacker.getCurrentPokemon().name+" uses "+move.name+"!\n"
        else: # we are the reciever
            if isinstance(move, Move.Swap): # they just swapped something out
                r_str += attacker.name+" withdrew "+move.swaped_out+"!\n"
                r_str += attacker.name+" sent out "+move.swaped_in+"!\n"
            elif isinstance(move, Move.Faint): # i've got good news
                r_str += move.pokemon.name+" fainted!\n"
            else:
                r_str += "The opposing "+attacker.getCurrentPokemon().name+" uses "+move.name+"!\n"
        return r_str

    def notify_move(self, attacker, move):
        if attacker is self.player1:
            self.player1.append_to_log(self.get_move_string(attacker, move, True))
            self.player2.append_to_log(self.get_move_string(attacker, move, False))
        elif attacker is self.player2:
            self.player1.append_to_log(self.get_move_string(attacker, move, False))
            self.player2.append_to_log(self.get_move_string(attacker, move, True))
        else:
            pass

    def notify_damage(self, victim, dmg):
        if victim is self.player1:
            self.player1.append_to_log("("+victim.getCurrentPokemon() + " lost "+str(dmg)+"% of its health!)")
            self.player2.append_to_log("(The opposing "+victim.getCurrentPokemon() + " lost "+str(dmg)+"% of its health!)")
        else:
            self.player2.append_to_log("(" + victim.getCurrentPokemon() + " lost " + str(dmg) + "% of its health!)")
            self.player1.append_to_log("(The opposing " + victim.getCurrentPokemon() + " lost " + str(dmg) + "% of its health!)")

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
        self.player1.initalizeGame(self)
        self.player2.initalizeGame(self)

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
                self.notify_move(self.player1, move1)
                dmg = self.player1.getCurrentPokemon().do_damage(self.player2.getCurrentPokemon(), move1)
                self.notify_damage(self.player2, dmg)
                if not self.player2.getCurrentPokemon().is_dead():
                    self.notify_move(self.player2, move2)
                    dmg = self.player2.getCurrentPokemon().do_damage(self.player1.getCurrentPokemon(), move2)
                    self.notify_damage(self.player1, dmg)
                else:
                    self.notify_move(self.player2, Move.Faint(self.player2.getCurrentPokemon()))

                if self.player1.getCurrentPokemon().is_dead():
                    self.notify_move(self.player1, Move.Faint(self.player1.getCurrentPokemon()))
            else:
                self.notify_move(self.player2, move2)
                dmg = self.player2.getCurrentPokemon().do_damage(self.player1.getCurrentPokemon(), move2)
                self.notify_damage(self.player1, dmg)
                if not self.player1.getCurrentPokemon().is_dead():
                    self.notify_move(self.player1, move1)
                    dmg = self.player1.getCurrentPokemon().do_damage(self.player2.getCurrentPokemon(), move1)
                    self.notify_damage(self.player2, dmg)
                else:
                    self.notify_move(self.player1, Move.Faint(self.player1.getCurrentPokemon()))

                if self.player2.getCurrentPokemon().is_dead():
                    self.notify_move(self.player2, Move.Faint(self.player2.getCurrentPokemon()))