from tictactoe import TicTacToe
import random

def dfs_state(start_state, goal):
    stack = [start_state]
    visited = set()
    while len(stack) > 0:
        state = stack.pop()
        if state.get_hash() not in visited:
            visited.add(state.get_hash())
            if goal(state):
                print("Visited:", len(visited))
                return state
            stack += state.get_children()
    print("Visited:", len(visited))
    return None

def dfs_recursive(state, visited, goal):
    visited.add(state.get_hash())
    if goal(state):
        return state
    for child in state.get_children():
        if child.get_hash() not in visited:
            found_state = dfs_recursive(child, visited, goal)
            if found_state is not None:
                return found_state
    return None

def dfs_move_undo(state, goal):
    if goal(state):
        return state
    terminal, terminal_result = state.is_terminal()
    if terminal:
        return None
    for move in state.get_moves():
        state.make_move(move)
        found_state = dfs_move_undo(state, goal)
        state.undo_move(move)
        if found_state is not None:
            return found_state
    return None

def dfs_general(state, visited, goal):
    visited.add(state.get_hash())
    if goal(visited):
        return visited
    for child in state.get_children():
        if child.get_hash() not in visited:
            found_visited = dfs_general(child, visited, goal)
            if found_visited is not None:
                return found_visited
    return None

def dfs_path(path, visited, goal):
    visited.add(tuple([state.get_hash() for state in path]))
    if goal(path):
        return path
    for child in path[-1].get_children():
        child_path = path + [child]
        if tuple([state.get_hash() for state in child_path]) not in visited:
            found_path = dfs_path(child_path, visited, goal)
            if found_path is not None:
                return found_path
    return None


def dfs_path_to_end(path, visited, end):
    visited.add(tuple([state.get_hash() for state in path]))
    if path[-1].board == end:
        return path
    for child in path[-1].get_children():
        child_path = path + [child]
        if tuple([state.get_hash() for state in child_path]) not in visited:
            found_path = dfs_path_to_end(child_path, visited, end)
            if found_path is not None:
                return found_path
    return None

def dfs_heuristic(path, visited, end, heuristic):
    visited.add(tuple([state.get_hash() for state in path]))
    if path[-1].board == end:
        return path
    ranked_children = sorted(path[-1].get_children(), key=heuristic)
    for child in ranked_children:
        child_path = path + [child]
        if tuple([state.get_hash() for state in child_path]) not in visited:
            found_path = dfs_heuristic(child_path, visited, end, heuristic)
            if found_path is not None:
                return found_path
    return None

def bfs_state(start_state, goal):
    queue = [start_state]
    visited = set()
    while len(queue) > 0:
        state = queue.pop()
        if state.get_hash() not in visited:
            if goal(state):
                print("Visited:", len(visited))
                return state
            visited.add(state.get_hash())
            queue = state.get_children() + queue
    print("Visited:", len(visited))
    return None

def bfs_path(start_state, goal):
    queue = [start_state]
    visited = set(queue)
    while len(queue) > 0:
        state = queue.pop()
        if goal(state):
            print("Visited:", len(visited))
            return state
        for child in state.get_children():
            if child.get_hash() not in visited:
                visited.add(child.get_hash())
                child.parent = state
                queue.insert(0, child)
    print("Visited:", len(visited))
    return None

def find_recorded_path(state):
    if state.parent is None:
        return [state]
    else:
        return find_recorded_path(state.parent) + [state]

#path = find_recorded_path(bfs_path(start_state, goal))

def A_star(start_state, end_state, heuristic):
    start_state.dist_from_start = 0
    prio_queue = [(start_state, 0)]
    visited = {}
    visited[start_state.get_hash()] = 0
    while len(prio_queue) > 0:
        state, value = prio_queue.pop()
        if state.board == end_state:
            print("Visited:", len(visited))
            return state
        for child in state.get_children():
            child.dist_from_start = state.dist_from_start + 1
            if child.get_hash() not in visited \
            or visited[child.get_hash()] > child.dist_from_start:
                visited[child.get_hash()] = child.dist_from_start
                child.parent = state
                prio_queue.append((child, child.dist_from_start \
                                    + heuristic(start_state, end_state)))
        prio_queue.sort(key=lambda x:x[1])
    print("Visited:", len(visited))
    return None

target_board = [[1,0,2],\
                [2,2,1],\
                [2,1,1]]

def goal_func(state):
    if state.board == target_board:
        print("goal satisfied")
        return True
    return False

ttt = TicTacToe()
print("DFS state:")
dfs_state(ttt, goal_func).print_board()

visited = set()
ttt = TicTacToe()
print("\nDFS recursive:")
dfs_recursive(ttt, visited, goal_func).print_board()
print("Visited:", len(visited))

def goal_func_general(v):
    if str(target_board) in v:
        print("goal satisfied")
        return True
    return False 
visited = set()
ttt = TicTacToe()
print("\nDFS general:")
print("Visited:", len(dfs_general(ttt, visited, goal_func_general)))

def goal_func_path(path):
    if path[-1].board == target_board:
        print("goal satisfied")
        return True
    return False
visited = set()
ttt = TicTacToe()
print("\nDFS path:")
path = [ttt]
path = dfs_path(path, visited, goal_func_path)
print("Visited:", len(visited))
for s in path:
    s.print_board()

visited = set()
ttt = TicTacToe()
print("\nDFS path to end:")
path = [ttt]
path = dfs_path_to_end(path, visited, target_board)
print("Visited:", len(visited))
for s in path:
    s.print_board()

def ttt_heuristic(state, tb=target_board):
    diff = 0
    for y in range(3):
        for x in range(3):
            if state.board[y][x] != tb[y][x]:
                diff += 1
    return diff
visited = set()
ttt = TicTacToe()
print("\nDFS heuristic:")
path = [ttt]
path = dfs_heuristic(path, visited, target_board, ttt_heuristic)
print("Visited:", len(visited))
for s in path:
    s.print_board()

def ttt_random_heuristic(state, tb=target_board):
    diff = 0
    for y in range(3):
        for x in range(3):
            if state.board[y][x] != tb[y][x] or random.random() < 0.5:
                diff += 1
    return diff
visited = set()
ttt = TicTacToe()
print("\nDFS with a random imperfect heuristic:")
path = [ttt]
path = dfs_heuristic(path, visited, target_board, ttt_random_heuristic)
print("Visited:", len(visited))
for s in path:
    s.print_board()

ttt = TicTacToe()
print("\nBFS state:")
bfs_state(ttt, goal_func).print_board()

ttt = TicTacToe()
print("\nBFS path:")
end_state = bfs_path(ttt, goal_func)
end_state.print_board()
for s in find_recorded_path(end_state):
    s.print_board()

ttt = TicTacToe()
print("\nA*:")
end_state = A_star(ttt, target_board, ttt_heuristic)
end_state.print_board()
for s in find_recorded_path(end_state):
    s.print_board()

ttt = TicTacToe()
print("\nA* random imperfect heuristic:")
end_state = A_star(ttt, target_board, ttt_random_heuristic)
end_state.print_board()
for s in find_recorded_path(end_state):
    s.print_board()