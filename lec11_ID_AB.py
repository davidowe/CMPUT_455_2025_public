from gomoku import Gomoku
import time
import numpy

visited_count = 0

def negamax_alpha_beta(state, alpha, beta, tt, move_heuristic=None):
    global visited_count
    visited_count += 1
    state_key = state.get_state_key()
    if state_key in tt:
        return tt[state_key]
    terminal, score = state.is_terminal_relative_score()
    if terminal:
        tt[state_key] = score
        return score
    value = -float('inf')
    ordered_moves = state.get_moves()
    if move_heuristic is not None:
        ordered_moves = sorted(ordered_moves, key=lambda x:move_heuristic(state, x), reverse=True)
    for move in ordered_moves:
        state.make_move(move)
        value = max(value, -negamax_alpha_beta(state, -beta, -alpha, tt, move_heuristic))
        state.undo_move(move)
        alpha = max(alpha, value)
        if alpha >= beta:
            tt[state_key] = value
            return value
    tt[state_key] = value
    return value

def adj_lines_move_heuristic(state, move):
    score = 0
    x = move[0]
    y = move[1]
    for dx, dy in [(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(0,-1)]:
        x1 = x + dx
        y1 = y + dy
        if x1 >= 0 and x1 < state.width and y1 >= 0 and y1 < state.height: 
            c = state.board[y1][x1]
            if c != 0:
                line_len = 0
                while x1 >= 0 and x1 < state.width and y1 >= 0 and y1 < state.height \
                        and state.board[y1][x1] == c:
                    line_len += 1
                    y1 += dy
                    x1 += dx
                score += line_len**2

    return score

def open_two_line_position_heuristic(state):
    score = 0
    for y in range(state.height):
        for x in range(state.width):
            c = state.board[y][x]
            if c != state.to_play:
                continue
            for dx, dy in [(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(0,-1)]:
                x1 = x + dx
                y1 = y + dy
                if x1 >= 0 and x1 < state.width and \
                    y1 >= 0 and y1 < state.height and \
                    state.board[y1][x1] == state.to_play: 
                    x2 = x1 + dx
                    y2 = y1 + dy
                    if x2 >= 0 and x2 < state.width and \
                        y2 >= 0 and y2 < state.height and \
                        state.board[y2][x2] == 0:
                        score += 1
    return numpy.tanh(score)

#Returns: score, valid
def negamax_alpha_beta_limited_depth(state, alpha, beta, \
                                     depth, max_depth, tt, pos_eval):
    #Stats
    global visited_count
    visited_count += 1
    #Check if the position is in the transposition table
    best_move = None
    state_key = state.get_state_key()
    #If the position is already solved, return the solved value
    if state_key in tt:
        value, valid, best_move = tt[state_key]
        if valid:
            return value, valid
    else:
        #Check if the position is terminal
        terminal, score = state.is_terminal_relative_score()
        if terminal:
            tt[state_key] = (score, terminal, None)
            return score, True
        #Check if we've reached the max depth
        if depth == max_depth:
            eval = pos_eval(state)
            tt[state_key] = (eval, False, None)
            return eval, False
    #If there is a recorded best move in the tt, search that first
    moves = state.get_moves()
    if best_move is not None:
        moves.remove(best_move)
        moves.insert(0,best_move)
    #Check all legal moves until a cutoff
    valid_result = True
    value = -float('inf')
    best_found_move = None
    for move in state.get_moves():
        #Recursive call
        state.make_move(move)
        child_value, valid_child = negamax_alpha_beta_limited_depth\
                    (state, -beta, -alpha, depth+1, max_depth, tt, pos_eval)
        state.undo_move(move)
        #Update value and record the best move found
        if -child_value > value:
            value = -child_value
            best_found_move = move
        #Record whether we encounter any heuristic values
        valid_result = valid_result and valid_child
        #Check for alpha beta cutoffs
        alpha = max(alpha, value)
        if alpha >= beta:
            tt[state_key] = (value, valid_result, best_found_move)
            return value, valid_result
    #No cutoffs, return result
    tt[state_key] = (value, valid_result, best_found_move)
    return value, valid_result

def iterative_deepening_AB(state, pos_eval):
    tt = {}
    max_depth = 0
    value = None
    while True:
        value, valid = negamax_alpha_beta_limited_depth(\
            state, -1, 1, 0, max_depth, tt, pos_eval)
        print("Depth:", max_depth, "\tTT size:", len(tt), "\tVisited:", visited_count, "\tRoot value:", value, "\tRoot best move:", tt[root.get_state_key()][2])
        if valid:
            return value
        max_depth += 1

w = 3
h = 4
l = 4

t0 = time.time()
root = Gomoku(w, h, l)
visited_count = 0
tt = {}
print("\nMinimax score for", w, h, l, "Gomoku using negamax with alpha beta pruning and a tt, \n\
      [-1,1] window, line counting move heuristic:", negamax_alpha_beta(root, -1, 1, tt, adj_lines_move_heuristic))
print("Took", round(time.time() - t0,2), "seconds")
print("Nodes visited:", visited_count)
print()

t0 = time.time()
root = Gomoku(w, h, l)
visited_count = 0
print("\nMinimax score for", w, h, l, "Gomoku using iterative deepening negamax alpha beta, \n\
      [-1,1] window, open two line position heuristic:", iterative_deepening_AB(root, open_two_line_position_heuristic))
print("Took", round(time.time() - t0,2), "seconds")
print("Nodes visited:", visited_count)