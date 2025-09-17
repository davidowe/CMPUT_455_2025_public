import matplotlib.pyplot as plt
import time
from tictactoe import TicTacToe

def update_stat(stats, key, depth, val=1):
    if key not in stats:
        stats[key] = []
    count_list = stats[key]
    while depth >= len(count_list):
        count_list.append(0)
    count_list[depth] += val

def count_states(state, stats, depth):
    update_stat(stats, "reachable", depth)

    is_terminal, winner = state.is_terminal()
    if is_terminal:
        update_stat(stats, "terminal", depth)
        if winner == 1:
            update_stat(stats, "p1_wins", depth)
        elif winner == 2:
            update_stat(stats, "p2_wins", depth)
        else:
            update_stat(stats, "draws", depth)

    children = state.get_children()
    for child in children:
        count_states(child, stats, depth+1)

stats = {}
print("\nExploring...")
t0 = time.time()
count_states(TicTacToe(), stats, 0)
print("Took", round(time.time()-t0, 2), "seconds to explore the state space.\n")

bg_color = (250/255, 245/255, 235/255)
plt.rcParams.update({
    "figure.facecolor" : bg_color,
    "axes.facecolor" : bg_color,
    "font.size" : 14,
    "ytick.labelsize" : 12,
    "figure.figsize" : (10,6)
})
plt.grid(True)
plt.xlabel('Depth')
plt.ylabel('Count')
plt.title('TicTacToe State Space Exploration')

for key, values in stats.items():
    print(key, "total:", sum(values))
    plt.plot(range(len(values)), values, label=key, linewidth=5)
plt.legend()
plt.savefig("tictactoe_state_space.png")

def count_states_DAG(state, stats, depth, transposition_table):
    state_key = state.get_state_key()
    if state_key in transposition_table:
        update_stat(stats, "tt_hit", depth)
        transposition_table[state_key] += 1
        return
    transposition_table[state_key] = 1

    update_stat(stats, "reachable", depth)

    is_terminal, winner = state.is_terminal()
    if is_terminal:
        update_stat(stats, "terminal", depth)
        if winner == 1:
            update_stat(stats, "p1_wins", depth)
        elif winner == 2:
            update_stat(stats, "p2_wins", depth)
        else:
            update_stat(stats, "draws", depth)

    children = state.get_children()
    for child in children:
        count_states_DAG(child, stats, depth+1, transposition_table)

stats_DAG = {}
transposition_table = {}
print("\nExploring DAG model...")
t0 = time.time()
count_states_DAG(TicTacToe(), stats_DAG, 0, transposition_table)
print("Took", round(time.time()-t0, 2), "seconds to explore the DAG state space.\n")

plt.clf()
plt.grid(True)
plt.xlabel('Depth')
plt.ylabel('Count')
for key, values in stats_DAG.items():
    print(key, "total:", sum(values))
    plt.plot(range(len(values)), values, label=key, linewidth=5)
plt.title('TicTacToe State Space Exploration DAG')
plt.legend()
plt.savefig("tictactoe_state_space_dag.png")

