class Gomoku:
    def __init__(self, width=7, height=7, winning_length=5):
        self.width = width
        self.height = height
        self.winning_length = winning_length
        self.to_play = 1
        self.board = []
        for y in range(height):
            self.board.append([0]*width)
        self.parent = None
    
    def make_move(self, move):
        self.board[move[1]][move[0]] = self.to_play
        self.to_play = 1 if self.to_play == 2 else 2

    def undo_move(self, move):
        self.board[move[1]][move[0]] = 0
        self.to_play = 1 if self.to_play == 2 else 2

    def get_moves(self):
        moves = []
        for y in range(self.height):
            moves += [(x, y) for x in range(self.width) if self.board[y][x] == 0]
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
        for y in range(self.height):
            for x in range(self.width):
                print(self.player_to_str(self.board[y][x]), end=" ")
            print()
        print("To play:", self.player_to_str(self.to_play))

    #Returns if the state is terminal, and the winner (None for draw)
    #Definitely not optimized
    #Gives full board draws to the second player as wins
    def is_terminal(self):
        for piece in [1, 2]:
            for y in range(self.height):
                for x in range(self.width):
                    #Horizontal lines
                    count = 0
                    for x1 in range(x, self.width):
                        if self.board[y][x1] == piece:
                            count += 1
                    if count >= self.winning_length:
                        return True, piece
                    #Vertical lines
                    count = 0
                    for y1 in range(y, self.height):
                        if self.board[y1][x] == piece:
                            count += 1
                    if count >= self.winning_length:
                        return True, piece
                    #Diagonal lines
                    count = 0
                    for d_offset in range(0, min(self.height-y,self.width-x)):
                        if self.board[y+d_offset][x+d_offset] == piece:
                            count += 1
                    if count >= self.winning_length:
                        return True, piece
                    #Anti-diagonal lines
                    count = 0
                    for ad_offset in range(0, min(y+1,self.width-x)):
                        if self.board[y-ad_offset][x+ad_offset] == piece:
                            count += 1
                    if count >= self.winning_length:
                        return True, piece
        #Check for draw
        any_empty = False
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 0:
                    any_empty = True
                    break
            if any_empty:
                break
        return not any_empty, 2
    
    def get_state_key(self):
        return str(self.board)
    
    def get_player(self):
        return self.to_play