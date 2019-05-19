import Pokemon
import Move
import Effects

class Agent:
    def get_percepts(self):
        pass
    def choose_turn(self):
        pass


class OneTurnAgent(Agent):
    def __init__(self, current_pokemon: Pokemon.Pokemon, inventory, opponent):
        self.inventory = inventory
        self.opponent = opponent
        self.current_pokemon = current_pokemon

    def get_max_harm_move(self, pokemon:Pokemon.Pokemon =None)->(int, Move.Move):
        '''
        Returns what move will inflict the maximum amount of damage to the enemy, given what we currently know
        :param pokemon: [OPTIONAL] returns the highest damage a specific pokemon can deal to the current enemy
        :return: A pair with the move to play
        '''

        if pokemon is not None:
            for move in pokemon.moveList:
                calc_dmg = pokemon.calculate_damage(self.opponent.current_pokemon, move)
                if calc_dmg > max_dmg:
                    max_dmg = calc_dmg
            return max_dmg

        # First, let's search all the moves for the current pokemon
        max_move = (-999999, None)
        for move in self.current_pokemon.moveList:
            current_dmg = self.current_pokemon.calculate_damage(self.opponent.current_pokemon, move)
            if current_dmg > max_move[0]:
                max_move = (current_dmg, move)

        # Next, let's see if there is another pokemon in our inventory that can deal more damage
        max_swap = (-999999, None)
        for pokemon in self.inventory:
            if pokemon == self.current_pokemon:
                continue  # we do not waste time redundantly checking max damage for the current pokemon
            current_swap = Move.Swap(self.current_pokemon, pokemon)
            current_dmg = self.get_max_harm_move(pokemon=pokemon)
            if current_dmg > max_swap[0]:
                max_swap = (current_dmg, current_swap)

        # Finally, compare the best swap to the best move, and return which one does the most damage
        if max_swap[0] > max_move[0]:
            return max_swap
        return max_move

    def choose_turn(self):
        _, move = self.get_max_harm_move()
        return move



