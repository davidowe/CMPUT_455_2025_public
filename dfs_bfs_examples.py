
def dfs_state(start_state, goal):
    stack = [start_state]
    visited = set()
    while len(stack) > 0:
        state = stack.pop()
        if state not in visited:
            visited.add(state)
            if goal(state):
                return state
            stack += state.children
    return None

def dfs_recursive(state, visited, goal):
    if goal(state):
        return state
    visited.add(state)
    for child in state.children:
        if child not in visited:
            found_state = dfs_recursive(child, visited, goal)
            if found_state is not None:
                return found_state
    return None

def dfs_general(state, visited, goal):
    visited.add(state)
    if goal(visited):
        return visited
    for child in state.children:
        if child not in visited:
            found_visited = dfs_general(child, visited, goal)
            if found_visited is not None:
                return found_visited
    return None

def dfs_path(path, visited, goal):
    if goal(path):
        return path
    visited.add(tuple(path))
    for child in path[-1].children:
        child_path = path + [child]
        if tuple(child_path) not in visited:
            found_path = dfs_path(child_path, visited, goal)
            if found_path is not None:
                return found_path
    return None


def dfs_path_to_end(path, visited, end):
    if path[-1] == end:
        return path
    visited.add(tuple(path))
    for child in path[-1].children:
        child_path = path + [child]
        if tuple(child_path) not in visited:
            found_path = dfs_path_to_end(child_path, visited, end)
            if found_path is not None:
                return found_path
    return None

def dfs_heuristic(path, visited, end, heuristic):
    if path[-1] == end:
        return path
    visited.add(tuple(path))
    ranked_children = sorted(path[-1].children, key=heuristic)
    for child in ranked_children:
        child_path = path + [child]
        if tuple(child_path) not in visited:
            found_path = dfs_heuristic(child_path, visited, \
                                        end, heuristic)
            if found_path is not None:
                return found_path
    return None

def bfs_state(start_state, goal):
    queue = [start_state]
    visited = set()
    while len(queue) > 0:
        state = queue.pop()
        if state not in visited:
            if goal(state):
                return state
            visited.add(state)
            queue = state.children + queue
    return None

def bfs_path(start_state, goal):
    queue = [start_state]
    visited = set(queue)
    while len(queue) > 0:
        state = queue.pop()
        if goal(state):
            return state
        for child in state.children:
            if child not in visited:
                visited.add(child)
                child.parent = state
                queue.insert(0, child)
    return None

def find_recorded_path(state):
    if state.parent is None:
        return [state]
    else:
        return find_recorded_path(state.parent) + [state]

#path = find_recorded_path(bfs_path(start_state, goal))

def A_star(start_state, end_state, distance, heuristic):
    prio_queue = [(start_state, 0)]
    visited = {}
    visited[start_state] = 0
    while len(prio_queue) > 0:
        state, value = prio_queue.pop()
        if state == end_state:
            return state
        for child in state.children:
            if child not in visited or visited[child] > distance(start_state, child):
                visited[child] = distance(start_state, child)
                child.parent = state
                prio_queue.append((child, distance(start_state, child) \
                                    + heuristic(start_state, end_state)))
        prio_queue.sort(key=lambda x:x[1], reverse=True)
    return None