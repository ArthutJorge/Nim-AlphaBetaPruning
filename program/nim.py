import random

class Nim:

    def __init__(self, initial = [1, 3, 5, 7]):
        
        '''
            Initialize game board. 
            Each game board has
                - 'piles'  : a list of how many elements remain in each pile
                - 'player' : 0 or 1 to indicate which player's turn
                - 'winner' : None, 0, or 1 to indicate who the winner is
        '''
        
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):

        '''
            self.available_actions(piles) takes a 'piles' list as input and returns all of the available actions '(i, j)' in that state. Action '(i, j)' represents the action of removing 'j' items from pile 'i'.
        '''
        actions = set()
        for i, count in enumerate(piles): 
            for j in range(1, count + 1):
                actions.add((i, j))
        return actions
    
    @classmethod
    def other_player(cls, player):

        '''
            self.other_player(player) returns the playe that is not 'player'. Assumes 'player' is either 0 or 1.
        '''

        return 0 if player == 1 else 1
    
    def switch_player(self):

        '''
            Switch the current player to the other player.
        '''
        self.player = Nim.other_player(self.player)

    def move(self, action):

        '''
            Make the move 'action' for the current player. 'action' must be a tuple '(i, j)'.
        '''
        
        i, j = action
        self.piles[i] -= j
        if(all(pile == 0 for pile in self.piles)):
            self.winner = self.other_player(self.player)
        self.switch_player()
        



class AlphaBetaPrunning:

    def choose_action(self, piles, depth, alpha, beta, isMaximizing):
        '''
            Determines the best move using Alpha-Beta Pruning.
        '''
        
        if depth == 0 or all(pile == 0 for pile in piles):  # base case
            return self.evaluate(piles, isMaximizing)

        best_action = None
        best_eval = float('-inf') if isMaximizing else float('inf')

        for action in Nim.available_actions(piles):
            new_piles = piles.copy() # creates a copy of the current state to simulate the action
            i, j = action
            new_piles[i] -= j  # apply move

            eval = self.choose_action(new_piles, depth - 1, alpha, beta, not isMaximizing)

            if (isMaximizing and eval > best_eval) or (not isMaximizing and eval < best_eval): # maximizing seeks higher eval, minimizing seeks lower eval
                best_eval = eval
                best_action = action

            if isMaximizing:
                alpha = max(alpha, best_eval)
            else:
                beta = min(beta, best_eval)

            if beta <= alpha:
                break # prune remaining branches since they won't affect the optimal decision

        # return the best action if at the root depth (initial call)
        return best_action if depth == 10 else best_eval

    def evaluate(self, piles, isMaximizing):
        '''
            Evaluate the current game state.
        '''
        if all(pile == 0 for pile in piles): 
            return 100 if isMaximizing else -100  # highest weight for a win, lowest for a loss

        if all(pile <= 1 for pile in piles):
            if sum(piles) % 2 == 1:  # maximizing aims to leave an odd number of piles with 1 piece 
                return -10 if isMaximizing else 10
            else:  
                return 10 if isMaximizing else -10
        
        nim_sum = 0
        for pile in piles:
            nim_sum ^= pile

        if nim_sum == 0: # losing position for current player if opponent plays optimally
            return 1 if isMaximizing else -1

        return 0 # neutral position


def play(ai, human = None):
    
    # if no player order set, chose human's order randomly
    if human is None:
        human = 0 if random.uniform(0, 1) < 0.5 else 1

    # create new game
    game = Nim()

    while True:

        # print contents of piles
        for i, pile in enumerate(game.piles):
            print(f'Pile {i} : {pile}')

        # compute available actions
        available_actions = Nim.available_actions(game.piles)

        # let human make a move
        if game.player == human:
            print('Your turn')
            while True:
                pile, count = map(int, input('Choose a pile and count: ').split())
                if (pile, count) in available_actions:
                    break
                print('Invalid move, try again')
        # have AI make a move
        else:
            print('AI turn')
            pile, count = ai.choose_action(game.piles, 10, float('-inf'), float('inf'), True)
            print(f'AI chose to take {count} from pile {pile}.')

        # make move
        game.move((pile, count))

        # check the winner
        if game.winner is not None:
            print('GAME OVER')
            winner = 'Human' if game.winner == human else 'AI'
            print(f'Winner is {winner}')
            break


play(AlphaBetaPrunning()) 
