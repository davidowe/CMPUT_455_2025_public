from tictactoe import TicTacToe
import math

def is_symmetric_about_vertical(state):
    for y in range(state.height):
        for x in range(math.ceil(state.width/2)):
            if state.board[y][x] != state.board[y][state.width-1-x]:
                return False
    return True

def generate_symmetric_state_about_vertical(state, sym_state):
    for y in range(state.height):
        for x in range(state.width):
            sym_state.board[y][x] = state.board[y][state.width-1-x]

def generate_symmetric_state_about_horizontal(state, sym_state):
    for y in range(state.height):
        for x in range(state.width):
            sym_state.board[y][x] = state.board[state.height-1-y][x]

def generate_symmetric_state_about_diagonal(state, sym_state):
    for y in range(state.height):
        for x in range(state.width):
            sym_state.board[y][x] = state.board[x][y]

def generate_symmetric_state_about_anti_diagonal(state, sym_state):
    for y in range(state.height):
        for x in range(state.width):
            sym_state.board[y][x] = state.board[state.width-1-x][state.height-1-y]

def generate_symmetric_state_about_90_rotation(state, sym_state):
    for y in range(state.height):
        for x in range(state.width):
            sym_state.board[y][x] = state.board[state.height-1-x][y]
    
def generate_symmetric_state_about_180_rotation(state, sym_state):
    for y in range(state.height):
        for x in range(state.width):
            sym_state.board[y][x] = state.board[state.height-1-y][state.width-1-x]

def generate_symmetric_state_about_270_rotation(state, sym_state):
    for y in range(state.height):
        for x in range(state.width):
            sym_state.board[y][x] = state.board[x][state.height-1-y]

ttt = TicTacToe([[2,0,1],[1,0,0],[0,2,1]],2)
ttt_symm = TicTacToe()

print("Identity:")
ttt.print_board()

print("\nAbout vertical:")
ttt.print_board()
generate_symmetric_state_about_vertical(ttt, ttt_symm)
ttt_symm.print_board()

print("\nAbout horizontal:")
ttt.print_board()
generate_symmetric_state_about_horizontal(ttt, ttt_symm)
ttt_symm.print_board()

print("\nAbout diagonal:")
ttt.print_board()
generate_symmetric_state_about_diagonal(ttt, ttt_symm)
ttt_symm.print_board()

print("\nAbout anti_diagonal:")
ttt.print_board()
generate_symmetric_state_about_anti_diagonal(ttt, ttt_symm)
ttt_symm.print_board()

print("\nAbout 90_rotation:")
ttt.print_board()
generate_symmetric_state_about_90_rotation(ttt, ttt_symm)
ttt_symm.print_board()

print("\nAbout 180_rotation:")
ttt.print_board()
generate_symmetric_state_about_180_rotation(ttt, ttt_symm)
ttt_symm.print_board()

print("\nAbout 270_rotation:")
ttt.print_board()
generate_symmetric_state_about_270_rotation(ttt, ttt_symm)
ttt_symm.print_board()

def count_non_symmetric_states_DAG(state, visited):
    if state.get_state_key() in visited:
        return
    sym = TicTacToe()
    for sym_generator in [generate_symmetric_state_about_vertical,\
                          generate_symmetric_state_about_horizontal,\
                          generate_symmetric_state_about_diagonal,\
                          generate_symmetric_state_about_anti_diagonal,\
                          generate_symmetric_state_about_90_rotation,\
                          generate_symmetric_state_about_180_rotation,\
                          generate_symmetric_state_about_270_rotation]:
        sym_generator(state, sym)
        if sym.get_state_key() in visited:
            return
    visited.add(state.get_state_key())
    for child in state.get_children():
        count_non_symmetric_states_DAG(child, visited)

print("\n\nThe number of symmetrically unique states in a DAG model of Tic Tac Toe:")
ttt = TicTacToe([[0]*3,[0]*3,[0]*3])
visited = set()
count_non_symmetric_states_DAG(ttt, visited)
print(len(visited))