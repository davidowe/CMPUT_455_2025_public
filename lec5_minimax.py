from tictactoe import TicTacToe
import time

def minimax(state, max_player):
    children = state.get_children()
    if len(children) == 0:
        return state.get_fixed_score()
    if state.get_player() == max_player:
        return max([minimax(child, max_player) for child in children])
    else:
        return min([minimax(child, max_player) for child in children])
        
def negamax(state):
    children = state.get_children()
    if len(children) == 0:
        return state.get_relative_score()
    return max([-negamax(child) for child in children])

def negamax_saved(state, strategy):
    terminal, winner = state.is_terminal()
    if terminal:
        return state.get_relative_score()
    max_score = None
    max_move = None
    for move in state.get_moves():
        state.make_move(move)
        child_score = -negamax_saved(state, strategy)
        state.undo_move(move)
        if max_score is None or child_score > max_score:
            max_score = child_score
            max_move = move
    strategy[state.get_state_key()] = max_move
    return max_score

def boolean_negamax(state, win_conditions):
    terminal, winner = state.is_terminal()
    if terminal:
        return win_conditions(state, winner)
    can_win = False
    for child in state.get_children():
        can_win = not boolean_negamax(child, win_conditions) or can_win
    return can_win

def boolean_negamax_cutoffs(state, win_conditions):
    terminal, winner = state.is_terminal()
    if terminal:
        return win_conditions(state, winner)
    can_win = False
    for child in state.get_children():
        can_win = can_win or not boolean_negamax_cutoffs(child, win_conditions)
    return can_win

t0 = time.time()
ttt = TicTacToe()
print("Minimax score for Tic Tac Toe:")
print(minimax(ttt, 1))
print("Took", round(time.time() - t0,2), "seconds")

t0 = time.time()
ttt = TicTacToe()
print("\nMinimax score for Tic Tac Toe (using negamax):")
print(negamax(ttt))
print("Took", round(time.time() - t0,2), "seconds")

t0 = time.time()
ttt = TicTacToe()
strategy = {}
print("\nMinimax score for Tic Tac Toe (using negamax saved):")
print(negamax_saved(ttt, strategy))
print("Took", round(time.time() - t0,2), "seconds")
ttt = TicTacToe()
print(strategy[ttt.get_state_key()])

def p1_must_win(state, winner):
    if state.get_player() == 1:
        return winner == 1
    else:
        return winner != 1

def p2_must_win(state, winner):
    if state.get_player() == 1:
        return winner != 2
    else:
        return winner == 2
    
t0 = time.time()
ttt = TicTacToe()
print("\nBoolean negamax to determine if p1 can always win:")
print(boolean_negamax(ttt, p1_must_win))
print("Took", round(time.time() - t0,2), "seconds")

t0 = time.time()
ttt = TicTacToe()
print("\nBoolean negamax to determine if p1 can always win or draw:")
print(boolean_negamax(ttt, p2_must_win))
print("Took", round(time.time() - t0,2), "seconds")

t0 = time.time()
ttt = TicTacToe()
print("\nBoolean negamax with cutoffs to determine if p1 can always win:")
print(boolean_negamax_cutoffs(ttt, p1_must_win))
print("Took", round(time.time() - t0,2), "seconds")

t0 = time.time()
ttt = TicTacToe()
print("\nBoolean negamax with cutoffs to determine if p1 can always win or draw:")
print(boolean_negamax_cutoffs(ttt, p2_must_win))
print("Took", round(time.time() - t0,2), "seconds")






def f1(state):
    terminal, winner = state.is_terminal()
    if terminal:
        return winner == state.to_play
    can_win = False
    for child in state.get_children():
        child_result = not f1(child)
        can_win = child_result or can_win
    return can_win

def f2(state):
    terminal, winner = state.is_terminal()
    if terminal:
        return winner == state.to_play
    for child in state.get_children():
        child_result = not f2(child)
        if child_result:
            return True
    return False


def foo(state, max_player, heuristic_ME):
    children = state.get_children()
    if len(children) == 0:
        return state.get_fixed_score()
    ordered_children = sorted(children, key=lambda x: heuristic_ME(x))
    if state.get_player() == max_player:
        return max([foo(child, max_player, heuristic_ME) for child in ordered_children])
    else:
        return min([foo(child, max_player, heuristic_ME) for child in ordered_children])