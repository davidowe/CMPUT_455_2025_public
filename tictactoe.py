class TicTacToe:
    def __init__(self, init_board = [[0]*3,[0]*3,[0]*3], init_to_play = 1):
        self.to_play = init_to_play
        self.board = init_board
        self.parent = None

    def get_children(self):
        children = []
        terminal, winner = self.is_terminal()
        if not terminal:
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == 0:
                        child_board = [list(self.board[y]) for y in range(3)]
                        child_board[y][x] = self.to_play
                        children.append(TicTacToe(child_board, 2 if self.to_play == 1 else 1))
        return children
    
    def make_move(self, move):
        self.board[move[0]][move[1]] = self.to_play
        self.to_play = 1 if self.to_play == 2 else 2

    def undo_move(self, move):
        self.board[move[0]][move[1]] = 0
        self.to_play = 1 if self.to_play == 2 else 2

    def get_moves(self):
        moves = []
        for y in range(3):
            moves += [(x, y) for x in range(3) if self.board[y][x] == 0]
        return moves

    def player_to_str(self, player):
        if player == 0:
            return "_"
        elif player == 1:
            return "X"
        elif player == 2:
            return "O"
        else:
            raise ValueError("Unknown board value")
    
    def print_board(self):
        for y in range(3):
            for x in range(3):
                print(self.player_to_str(self.board[y][x]), end=" ")
            print()
        print("To play:", self.player_to_str(self.to_play))

    #Returns if the state is terminal, and the winner (None for draw)
    def is_terminal(self):
        for piece in [1, 2]:
            #Horizontal lines
            for y in range(3):
                if self.board[y][0] == piece and self.board[y][1] == piece and self.board[y][2] == piece:
                    return True, piece
            #Vertical lines
            for x in range(3):
                if self.board[0][x] == piece and self.board[1][x] == piece and self.board[2][x] == piece:
                    return True, piece
            #Diagonal line
            if self.board[0][0] == piece and self.board[1][1] == piece and self.board[2][2] == piece:
                return True, piece
            #Anti-diagonal line
            if self.board[0][2] == piece and self.board[1][1] == piece and self.board[2][0] == piece:
                return True, piece
        #Check for draw
        any_empty = False
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 0:
                    any_empty = True
                    break
            if any_empty:
                break
        return not any_empty, None
    
    def get_state_key(self):
        return str(self.board)