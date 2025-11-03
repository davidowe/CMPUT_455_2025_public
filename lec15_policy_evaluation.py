import random
import time

score_tt = {}
#returns score, num dice remaining
def score_dice(dice):
    global score_tt
    counts = [0] * 6
    for roll in dice:
        counts[roll-1] += 1
    if counts == [1, 1, 1, 1, 1, 1]:
        return 1500, 6
    key = str(counts)
    if key in score_tt:
        return score_tt[key][0], score_tt[key][1]
    num_triples = 0
    num_pairs = 0
    largest_of_a_kind = 0
    triple_num = 0
    num_ones = counts[0]
    num_fives = counts[4]
    
    for i, count in enumerate(counts):
        if count > largest_of_a_kind:
            largest_of_a_kind = count
        if count == 2:
            num_pairs += 1
        if count == 3:
            num_triples += 1
            triple_num = i+1

    if num_triples == 2:
        score_tt[key] = (2500, 6)
        return 2500, 6
    if num_pairs == 3 or (num_pairs == 1 and largest_of_a_kind == 4):
        score_tt[key] = (1500, 6)
        return 1500, 6
    
    score = 0
    num_dice = len(dice)
    if largest_of_a_kind >= 4:
        score += 1000 * (largest_of_a_kind-3)
        num_dice -= largest_of_a_kind
    if num_triples == 1 and triple_num != 1:
         score += 100 * triple_num
         num_dice -= 3
    if num_ones <= 3:
        score += 100*num_ones
        num_dice -= num_ones
    if num_fives < 3:
        score += 50*num_fives
        num_dice -= num_fives
    if score == 0:
        num_dice = 0
    elif num_dice == 0:
        num_dice = 6
    score_tt[key] = (score, num_dice)
    return score, num_dice


def estimate_farkle_roll_EV(num_dice, num_samples=1000000):
    score_total = 0
    farkle_total = 0
    for i in range(num_samples):
        dice = [random.randint(1, 6) for _ in range(num_dice)]
        score, _ = score_dice(dice)
        score_total += score
        if score == 0:
            farkle_total += 1
    return score_total / num_samples, farkle_total / num_samples

#for i in range(1, 7):
#    print(estimate_farkle_roll_EV(i))

def random_walk(state):
    terminal, winner = state.is_terminal()
    if terminal:
        return winner
    moves = state.get_moves()
    rand_move = moves[random.randint(0,len(moves)-1)]
    state.make_move(rand_move)
    child_result = random_walk(state)
    state.undo_move(rand_move)
    return child_result

def random_walk_policies(state, player_policy, opponent_policy, epsilon=0):
    terminal, winner = state.is_terminal()
    if terminal:
        return winner
    if random.random() < epsilon:
        policy_move = random_policy(state)
    else:
        policy_move = player_policy(state)
    state.make_move(policy_move)
    child_result = random_walk_policies(state, opponent_policy, player_policy)
    state.undo_move(policy_move)
    return child_result

from tictactoe import TicTacToe

def test_matchup(p1_label, p1_policy, p2_label, p2_policy, epsilon=0, num_samples=10000):
    p1_wr = None
    print("\nTic Tac Toe random walks results from", num_samples, "samples, epsilon", epsilon)
    for i in range(2):
        print("\nP1", p1_label, "v.s.", "P2", p2_label)
        p1_wins = 0
        p2_wins = 0
        draws = 0
        ttt = TicTacToe()
        for i in range(num_samples):
            winner = random_walk_policies(ttt, p1_policy, p2_policy, epsilon)
            if winner is None:
                draws += 1
            elif winner == 1:
                p1_wins += 1
            else:
                p2_wins += 1

        print("P1 wins:", p1_wins/num_samples, "P2 wins:", p2_wins/num_samples, "Draws:", draws/num_samples)
        tmp_policy = p2_policy
        tmp_label = p2_label
        p2_policy = p1_policy
        p2_label = p1_label
        p1_policy = tmp_policy
        p1_label = tmp_label
        if p1_wr is None:
            p1_wr = p1_wins/num_samples
    return p1_wr, p1_wins/num_samples

def random_policy(state):
    moves = state.get_moves()
    return moves[random.randint(0,len(moves)-1)]

def first_move_policy(state):
    return state.get_moves()[0]

#Used for tic tac toe, return the move which complete a line of three if possible, otherwise return first available move
def greedy_policy(state):
    moves = state.get_moves()
    for move in moves:
        state.make_move(move)
        is_terminal, winner = state.is_terminal()
        state.undo_move(move)
        if is_terminal and winner == state.get_player():
            return move
    return moves[0]

def probabilistic_policy_corner(state):
    scores = [5, 1,  5,\
              1, 10, 1,\
              5, 1,  5]
    moves = []
    for y in range(3):
        for x in range(3):
            moves.append((x, y))
            if state.board[y][x] != 0:
                scores[y*3+x] = 0
                continue
            state.make_move((x, y))
            is_terminal, _ = state.is_terminal()
            state.undo_move((x, y))
            if is_terminal:
                scores[y*3+x] += 100
    return random.choices(moves, scores, k=1)[0]
    
def probabilistic_policy_edge(state):
    scores = [1, 5,  1,\
              5, 10, 5,\
              1, 5,  1]
    moves = []
    for y in range(3):
        for x in range(3):
            moves.append((x, y))
            if state.board[y][x] != 0:
                scores[y*3+x] = 0
                continue
            state.make_move((x, y))
            is_terminal, _ = state.is_terminal()
            state.undo_move((x, y))
            if is_terminal:
                scores[y*3+x] += 100
    return random.choices(moves, scores, k=1)[0]

def tournament(policies, labels, num_samples=10000):
    results = []
    for i in range(len(policies)):
        results.append(["--"]*len(policies))
    for i in range(len(policies)):
        for j in range(i, len(policies)):
            p1, p2 = test_matchup(labels[i] ,policies[i], labels[j], policies[j], num_samples=num_samples)
            results[i][j] = str(int(round(p1,2)*100))
            results[j][i] = str(int(round(p2,2)*100))
    print(" | ".join(labels))
    for i in range(len(policies)):
        for result in results[i]:
            if result == "100":
                print("100 | ", end="")
            else:
                print(result, " | ", end="")
        print()
        if i < len(policies)-1:
            print("_"*len(results[i]*6))
    return results

#tournament([random_policy, greedy_policy, probabilistic_policy_corner, probabilistic_policy_edge], ["random", "greedy", "corner", "edge"])

def flat_mc(state, turn_time_budget=0.1):
    t0 = time.time()
    moves = state.get_moves()
    move_i = 0
    visits = [0]*len(moves)
    score_totals = [0]*len(moves)
    while time.time()-t0 < turn_time_budget-0.01:
        state.make_move(moves[move_i])
        result = random_walk(state)
        state.undo_move(moves[move_i])
        visits[move_i] += 1
        if result == state.to_play:
            score_totals[move_i] += 1
        elif result == 3-state.to_play:
            score_totals[move_i] -= 1
        move_i = (move_i + 1) % len(moves)
    #state.print_board()
    #print("Total samples:", sum(visits))
    #for i in range(len(moves)):
    #    print(moves[i], round(score_totals[i]/visits[i],2))
    #print()
    max_score = -float('inf')
    max_i = 0
    for i in range(len(moves)):
        score_av = score_totals[i]/visits[i]
        if score_av > max_score:
            max_score = score_av
            max_i = i
    return moves[max_i]

tt = {}
def negamax_alpha_beta(state, alpha, beta):
    global tt
    state_key = state.get_state_key()
    score = state.get_relative_score()
    if score is not None:
        tt[state_key] = (score, None)
        return score, None
    value = -float('inf')
    best_move = None
    for move in state.get_moves():
        state.make_move(move)
        child_value, child_move = negamax_alpha_beta(state, -beta, -alpha)
        if -child_value > value:
            best_move = move
        value = max(value, -child_value)
        alpha = max(alpha, value)
        state.undo_move(move)
        if alpha >= beta:
            tt[state_key] = (value, best_move)
            return value, best_move
    tt[state_key] = (value, best_move)
    return value, best_move

def perfect_policy(state):
    val, move = negamax_alpha_beta(state, -1, 1)
    return move

test_matchup("Random", random_policy, "Perfect", perfect_policy, epsilon=0, num_samples=1000)