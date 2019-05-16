from abc import abstractmethod

import Pokemon
import Move
import random

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
    log: str = ""
    opponent = None

    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

    def initialize_game(self, session)->Move:
        self.session = session
        for pokemon in self.inventory:
            self.append_to_log(pokemon.get_info_str())
        if self.session.player1 is self:
            self.opponent = self.session.player2
        else:
            self.opponent = self.session.player1

    def append_to_log(self, log_str: str):
        self.log += log_str

    def life_check(self)->bool:
        for pokemon in self.inventory:
            if not pokemon.is_dead():
                return False
        return True

    def get_turn(self) -> Move.Move:  # this will return some move that will be applyed during play
        pass  # it may also apply an internal adjustments, such as taking a pokemon out of battle

    def get_current_pokemon(self) -> Pokemon.Pokemon:
        pass

    def request_backup(self) -> Move:  # this will return true or false depending on whether the player can continue
        pass

    def swap_request(self) -> Move.Swap:
        pass


class HumanPlayer(Player):
    def __init__(self, name, inventory):
        """

        :param name: Name of this player
        :param inventory: A list of all the pokemon the player drew from his deck

        The current pokemon will be selected as the first pokemon in the deck for now.
        """
        super(HumanPlayer, self).__init__(name, inventory)
        self.currentPokemon = None

    def get_turn(self):
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
            return self.currentPokemon.moveList[int(choice)-1]  # return the move we selected from our list

    def set_current_pokemon(self, index):
        self.currentPokemon = self.inventory[index]

    def get_current_pokemon(self)->Pokemon.Pokemon:
        return self.currentPokemon

    def swap_request(self)->Move.Swap:
        old_pokemon = self.currentPokemon
        old_pokemon.reset_stat_stage()
        index = 1
        invalid_choice = True
        while invalid_choice:
            for pokemon in self.inventory:
                if not pokemon.is_dead():
                    print(str(index)+". "+pokemon.name)
                index += 1
            choice = input("Enter a number to select a pokemon:")
            selected_pok = self.inventory[int(choice)-1]
            if not selected_pok.is_dead():
                invalid_choice = False
                self.set_current_pokemon(int(choice) - 1)
        return Move.Swap(old_pokemon, self.currentPokemon)

    def request_backup(self)->Move:
        if self.life_check():
            print("Your inventory is depleted")
            return None
        print("Your selected pokemon has fainted in battle, please select another: ")
        return self.swap_request()

    def initialize_game(self, session)->Move:
        super(HumanPlayer, self).initialize_game(session)
        return self.swap_request()  # request our current pokemon


class RandomPlayer(Player):
    def __init__(self, name):
        super(RandomPlayer, self).__init__(name, [Pokemon.get_random_pokemon() for _ in range(6)])
        self.currentPokemon = None

    def initialize_game(self, session):
        super(RandomPlayer, self).initialize_game(session)
        self.currentPokemon = random.choice(self.inventory)
        return Move.Swap(None, self.get_current_pokemon())

    def get_turn(self) -> Move.Move:
        number_of_moves = len(self.get_current_pokemon().moveList)
        choice = random.randint(0, number_of_moves)
        if choice == number_of_moves:
            return self.swap_request()
        return self.get_current_pokemon().moveList[choice]

    def get_current_pokemon(self) -> Pokemon.Pokemon:
        return self.currentPokemon

    def request_backup(self) -> Move:
        if self.life_check():
            return None
        return self.swap_request()

    def swap_request(self) -> Move.Swap:
        old_pokemon = self.get_current_pokemon()
        old_pokemon.reset_stat_stage()
        living = [pok for pok in self.inventory if not pok.is_dead()]
        new_pokemon = random.choice(living)
        self.currentPokemon = new_pokemon
        return Move.Swap(old_pokemon, new_pokemon)


class GameSession:
    @staticmethod
    def get_move_string(attacker, move, is_friendly)->str:
        r_str = ""
        if is_friendly:  # we are the attacker
            if isinstance(move, Move.Swap):  # we just swapped something out
                # r_str += attacker.name+" withdrew "+move.swaped_out+"\n"
                r_str += "Go! "+move.swaped_in.name+"!\n"
            elif isinstance(move, Move.Faint):  # i've got bad news
                r_str += move.pokemon.name + " fainted!\n"
            else:  # we've attacked our target
                r_str += attacker.get_current_pokemon().name + " uses " + move.name + "!\n"
        else:  # we are the receiver
            if isinstance(move, Move.Swap):  # they just swapped something out
                if not (move.swaped_out is None or move.swaped_out.is_dead):
                    r_str += attacker.name+" withdrew "+move.swaped_out.name+"!\n"
                r_str += attacker.name+" sent out "+move.swaped_in.name+"!\n"
            elif isinstance(move, Move.Faint):  # i've got good news
                r_str += move.pokemon.name+" fainted!\n"
            else:
                r_str += "The opposing " + attacker.get_current_pokemon().name + " uses " + move.name + "!\n"
        return r_str

    def notify_move(self, attacker, move):
        if attacker is self.player1:
            self.player1.append_to_log(self.get_move_string(attacker, move, True))
            self.player2.append_to_log(self.get_move_string(attacker, move, False))
        elif attacker is self.player2:
            self.player1.append_to_log(self.get_move_string(attacker, move, False))
            self.player2.append_to_log(self.get_move_string(attacker, move, True))
        self.log += self.get_move_string(attacker, move, False)

    def notify_effect(self, attacker, effect):
        pass

    def notify_damage(self, victim, dmg):
        if dmg == 0.0:
            return ""
        if victim is self.player1:
            self.player1.append_to_log("(" + victim.get_current_pokemon().name + " lost " + str("%.1f" % round(dmg, 1))
                                       + "% of its health!)\n")
            self.player2.append_to_log("(The opposing " + victim.get_current_pokemon().name + " lost "
                                       + str("%.1f" % round(dmg, 1)) + "% of its health!)\n")
        else:
            self.player2.append_to_log("(" + victim.get_current_pokemon().name + " lost " + str("%.1f" % round(dmg, 1))
                                       + "% of its health!)\n")
            self.player1.append_to_log("(The opposing " + victim.get_current_pokemon().name + " lost "
                                       + str("%.1f" % round(dmg, 1)) + "% of its health!)\n")
        self.log += ("(" + victim.get_current_pokemon().name + " lost " + str("%.1f" % round(dmg, 1))
                     + "% of its health!)\n")

    def notify_turn(self, num):
        self.player1.append_to_log("Turn "+str(num)+"\n")
        self.player2.append_to_log("Turn " + str(num)+"\n")
        self.log += "Turn "+str(num)+"\n"

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.log = ""
        self.lastCmd = ""
        self.winner = None

    def get_victor(self):
        return self.winner

    def perform_turn(self):
        # TODO: when a pokemon cannot play, we need to make sure it can't apply damage to it's oponent.

        self.player1.get_current_pokemon().apply_effect()  # update the effects either pokemon may have
        self.player2.get_current_pokemon().apply_effect()
        move1 = self.player1.get_turn()  # retrieve the chosen move.
        move2 = self.player2.get_turn()

        if ((move1.priority > move2.priority) or
            (move1.priority == move2.priority and
             self.player1.get_current_pokemon().get_stat("Speed") > self.player2.get_current_pokemon().get_stat("Speed"))):

            self.notify_move(self.player1, move1)
            dmg, _, _ = self.player1.get_current_pokemon().apply_damage(self.player2.get_current_pokemon(), move1)
            self.notify_damage(self.player2, dmg)
            if not self.player2.get_current_pokemon().is_dead():
                self.notify_move(self.player2, move2)
                dmg, _, _ = self.player2.get_current_pokemon().apply_damage(self.player1.get_current_pokemon(), move2)
                self.notify_damage(self.player1, dmg)
            else:
                self.notify_move(self.player2, Move.Faint(self.player2.get_current_pokemon()))

            if self.player1.get_current_pokemon().is_dead():
                self.notify_move(self.player1, Move.Faint(self.player1.get_current_pokemon()))
        else:
            self.notify_move(self.player2, move2)
            dmg, _, _ = self.player2.get_current_pokemon().apply_damage(self.player1.get_current_pokemon(), move2)
            self.notify_damage(self.player1, dmg)
            if not self.player1.get_current_pokemon().is_dead():
                self.notify_move(self.player1, move1)
                dmg, _, _ = self.player1.get_current_pokemon().apply_damage(self.player2.get_current_pokemon(), move1)
                self.notify_damage(self.player2, dmg)
            else:
                self.notify_move(self.player1, Move.Faint(self.player1.get_current_pokemon()))

            if self.player2.get_current_pokemon().is_dead():
                self.notify_move(self.player2, Move.Faint(self.player2.get_current_pokemon()))

    def run_game(self):
        self.notify_move(self.player1, self.player1.initialize_game(self))
        self.notify_move(self.player2, self.player2.initialize_game(self))
        turn = 1
        while True:
            self.notify_turn(turn)
            if self.player1.get_current_pokemon().is_dead():
                result = self.player1.request_backup()
                if result is None:  # if the opponent has no more pokemon to pull
                    self.winner = self.player2
                    return self.player2
                self.notify_move(self.player1, result)

            if self.player2.get_current_pokemon().is_dead():
                result = self.player2.request_backup()
                if result is None:  # if the opponent has no more pokemon to pull
                    self.winner = self.player1
                    return self.player1
                self.notify_move(self.player2, result)
            self.perform_turn()
            turn += 1


print("Initializing Session")
gs = GameSession(RandomPlayer("p1"), RandomPlayer("p2"))
print("Ready")
print("Commencing Fight")
victor = gs.run_game()
print(gs.player1.log)
print("Fight Complete")
print(victor.name+" is the winner")
