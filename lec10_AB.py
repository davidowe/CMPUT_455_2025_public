from tictactoe import TicTacToe
import time

visited_count = 0

def negamax(state):
    global visited_count
    visited_count += 1
    children = state.get_children()
    if len(children) == 0:
        return state.get_relative_score()
    return max([-negamax(child) for child in children])

def negamax_max_value_cutoffs(state, max_value):
    global visited_count
    visited_count += 1
    children = state.get_children()
    if len(children) == 0:
        return state.get_relative_score()
    value = None
    for child in children:
        child_result = -negamax_max_value_cutoffs(child, max_value)
        if value is None or child_result > value:
            value = child_result
        if value == max_value:
            return value
    return value

def minimax_alpha_beta(state, maximizing, alpha, beta):
    global visited_count
    visited_count += 1
    children = state.get_children()
    if len(children) == 0:
        return state.get_fixed_score()
    if maximizing:
        value = -float('inf')
        for child in children:
            value = max(value, minimax_alpha_beta(child, not maximizing, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                return value
    else:
        value = float('inf')
        for child in children:
            value = min(value, minimax_alpha_beta(child, not maximizing, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                return value
    return value

def negamax_alpha_beta(state, alpha, beta):
    global visited_count
    visited_count += 1
    children = state.get_children()
    if len(children) == 0:
        return state.get_relative_score()
    value = -float('inf')
    for child in children:
        value = max(value, -negamax_alpha_beta(child, -beta, -alpha))
        alpha = max(alpha, value)
        if alpha >= beta:
            return value
    return value

position = [[0,0,0],[0,0,0],[0,0,0]]
player = 1

t0 = time.time()
ttt = TicTacToe([list(x) for x in position], player)
visited_count = 0
print("\nMinimax score for Tic Tac Toe (using negamax):")
print(negamax(ttt))
print("Took", round(time.time() - t0,2), "seconds")
print("Nodes visited:", visited_count)

t0 = time.time()
ttt = TicTacToe([list(x) for x in position], player)
visited_count = 0
print("\nMinimax score for Tic Tac Toe (using negamax with max value cutoffs):")
print(negamax_max_value_cutoffs(ttt, 1))
print("Took", round(time.time() - t0,2), "seconds")
print("Nodes visited:", visited_count)

t0 = time.time()
ttt = TicTacToe([list(x) for x in position], player)
visited_count = 0
print("\nMinimax score for Tic Tac Toe (using minimax with alpha beta pruning):")
print(minimax_alpha_beta(ttt, player == 1, -float('inf'), float('inf')))
print("Took", round(time.time() - t0,2), "seconds")
print("Nodes visited:", visited_count)

t0 = time.time()
ttt = TicTacToe([list(x) for x in position], player)
visited_count = 0
print("\nMinimax score for Tic Tac Toe (using negamax with alpha beta pruning):")
print(negamax_alpha_beta(ttt, -float('inf'), float('inf')))
print("Took", round(time.time() - t0,2), "seconds")
print("Nodes visited:", visited_count)

t0 = time.time()
ttt = TicTacToe([list(x) for x in position], player)
visited_count = 0
print("\nMinimax score for Tic Tac Toe (using minimax with alpha beta pruning, [-1,1] window):")
print(minimax_alpha_beta(ttt, player == 1, -1, 1))
print("Took", round(time.time() - t0,2), "seconds")
print("Nodes visited:", visited_count)

t0 = time.time()
ttt = TicTacToe([list(x) for x in position], player)
visited_count = 0
print("\nMinimax score for Tic Tac Toe (using negamax with alpha beta pruning, [-1,1] window):")
print(negamax_alpha_beta(ttt, -1, 1))
print("Took", round(time.time() - t0,2), "seconds")
print("Nodes visited:", visited_count)