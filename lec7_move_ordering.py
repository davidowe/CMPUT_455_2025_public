from gomoku import Gomoku
import time
import signal

def boolean_negamax_cutoffs(state, win_conditions):
    global visited, imperfect_moves
    visited += 1
    terminal, winner = state.is_terminal()
    if terminal:
        return win_conditions(state, winner)
    for i, move in enumerate(state.get_moves()):
        state.make_move(move)
        if not boolean_negamax_cutoffs(state, win_conditions):
            state.undo_move(move)
            imperfect_moves += i
            return True
        state.undo_move(move)
    return False

def boolean_negamax_move_ordering(state, win_conditions, heuristic):
    global visited, imperfect_moves
    visited += 1
    terminal, winner = state.is_terminal()
    if terminal:
        return win_conditions(state, winner)
    ordered_moves = sorted(state.get_moves(), key=lambda x: heuristic(state, x), reverse=True)
    for i, move in enumerate(ordered_moves):
        state.make_move(move)
        if not boolean_negamax_move_ordering(state, win_conditions, heuristic):
            state.undo_move(move)
            imperfect_moves += i
            return True
        state.undo_move(move)
    return False

def most_neighbours_heuristic(state, move):
    score = 0
    x = move[0]
    y = move[1]
    if x > 0 and state.board[y][x-1] != 0:
        score += 1
    if x < state.width-1 and state.board[y][x+1] != 0:
        score += 1
    if y > 0 and state.board[y-1][x] != 0:
        score += 1
    if y < state.height-1 and state.board[y+1][x] != 0:
        score += 1
    if x > 0 and y > 0 and state.board[y-1][x-1] != 0:
        score += 1
    if x > 0 and y < state.height-1 and state.board[y+1][x-1] != 0:
        score += 1
    if x < state.width-1 and y > 0 and state.board[y-1][x+1] != 0:
        score += 1
    if x < state.width-1 and y < state.height-1 and state.board[y+1][x+1] != 0:
        score += 1
    return score

def adj_lines_heuristic(state, move):
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

def p1_must_win(state, winner):
    if state.get_player() == 1:
        return winner == 1
    else:
        return winner != 1

w = 3
h = 4
l = 4
print("Searching for whether p1 can always win on", w, "x", h, "Gomoku with winning line lengths of", l, "\n")

print("Boolean negamax with arbitrary move ordering")
t0 = time.time()
gomoku = Gomoku(w, h, l)
visited = 0
imperfect_moves = 0
print(boolean_negamax_cutoffs(gomoku, p1_must_win))
print("Took", round(time.time() - t0,2), "seconds, visited", visited, "nodes, imperfect moves searched:", imperfect_moves, "\n")

t0 = time.time()
gomoku = Gomoku(w, h, l)
visited = 0
imperfect_moves = 0
print("Boolean negamax with neighbour counting heuristic move ordering")
print(boolean_negamax_move_ordering(gomoku, p1_must_win, most_neighbours_heuristic))
print("Took", round(time.time() - t0,2), "seconds, visited", visited, "nodes, imperfect moves searched:", imperfect_moves, "\n")

print("Boolean negamax with line length counting heuristic move ordering")
t0 = time.time()
gomoku = Gomoku(w, h, l)
visited = 0
imperfect_moves = 0
print(boolean_negamax_move_ordering(gomoku, p1_must_win, adj_lines_heuristic))
print("Took", round(time.time() - t0,2), "seconds, visited", visited, "nodes, imperfect moves searched:", imperfect_moves, "\n")

