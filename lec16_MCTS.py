import random
import time
import math
from tictactoe import TicTacToe

class MCTS_node:
    def __init__(self, state):
        self.visits = 0
        self.score_total = 0
        self.children = []
        self.state = state.get_copy()

def random_walk(state): # returns the relative score
    score = state.get_relative_score()
    if score is not None:
        return score
    moves = state.get_moves()
    rand_move = moves[random.randint(0,len(moves)-1)]
    state.make_move(rand_move)
    score = -random_walk(state)
    state.undo_move(rand_move)
    return score

def UCB_selection(node, c=1):
    max_ucb = -float('inf')
    max_i = 0
    for i, child in enumerate(node.children):
        if child.visits == 0:
            return node.children[i]
        ucb_i = -child.score_total/child.visits+c*math.sqrt(math.log(node.visits)/child.visits)
        if ucb_i > max_ucb:
            max_ucb = ucb_i
            max_i = i
    return node.children[max_i]

def expansion(node):
    score = node.state.get_relative_score()
    if score is not None: #terminal node
        return -score
    moves = node.state.get_moves()
    for move in moves:
        node.state.make_move(move)
        node.children.append(MCTS_node(node.state))
        node.state.undo_move(move)

    # Simulation:
    child = UCB_selection(node)
    child.score_total += random_walk(child.state)
    child.visits = 1
    return child.score_total

def selection(node):
    if len(node.children) == 0:
        score = -expansion(node)
    else:
        score = -selection(UCB_selection(node))
    node.score_total += score
    node.visits += 1
    return score

def MCTS_policy(state, time_budget=0.1):
    t0 = time.time()
    root_node = MCTS_node(state)
    while time.time()-t0 < time_budget-0.01:
        selection(root_node)
    best_i = 0
    most_visits = 0
    for i, child in enumerate(root_node.children):
        if child.visits > most_visits:
            best_i = i
            most_visits = child.visits
    return state.get_moves()[best_i]

def random_walk_policies(state, player_policy, opponent_policy):
    terminal, winner = state.is_terminal()
    if terminal:
        return winner
    policy_move = player_policy(state)
    state.make_move(policy_move)
    child_result = random_walk_policies(state, opponent_policy, player_policy)
    state.undo_move(policy_move)
    return child_result

def test_matchup(p1_label, p1_policy, p2_label, p2_policy, num_samples=10000):
    p1_wr = None
    print("\nTic Tac Toe random walks results from", num_samples, "samples")
    for i in range(2):
        print("\nP1", p1_label, "v.s.", "P2", p2_label)
        p1_wins = 0
        p2_wins = 0
        draws = 0
        ttt = TicTacToe()
        for i in range(num_samples):
            winner = random_walk_policies(ttt, p1_policy, p2_policy)
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

def flat_mc(state, turn_time_budget=0.1):
    t0 = time.time()
    moves = state.get_moves()
    move_i = 0
    visits = [0]*len(moves)
    score_totals = [0]*len(moves)
    while time.time()-t0 < turn_time_budget-0.01:
        state.make_move(moves[move_i])
        score_totals[move_i] -= random_walk(state)
        state.undo_move(moves[move_i])
        visits[move_i] += 1
        move_i = (move_i + 1) % len(moves)
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
    _, move = negamax_alpha_beta(state, -1, 1)
    return move

test_matchup("Flat MC", flat_mc, "MCTS", MCTS_policy, num_samples=10)
#test_matchup("Random", random_policy, "MCTS", MCTS_policy, num_samples=1000)
#test_matchup("Perfect", perfect_policy, "MCTS", MCTS_policy, num_samples=1000)
#test_matchup("Perfect", perfect_policy, "Flat MC", flat_mc, num_samples=1000)
#test_matchup("Random", random_policy, "Flat MC", flat_mc, num_samples=1000)
#test_matchup("Flat MC", flat_mc, "Flat MC", flat_mc, num_samples=1000)
#test_matchup("MCTS", MCTS_policy, "MCTS", MCTS_policy, num_samples=1000)
