def dfs(problem):
    routes = []
    found = {problem.get_start_state()}
    stack = [[problem.get_start_state()]]
    while stack:
        path = stack.pop()
        u = path[-1]  # path の最後のノード
        for v in problem.next_states(u):
            if problem.is_goal(v):
                routes.append(path + [v])
            elif v not in found:
                found.add(v)
                stack.append(path + [v])
    return routes
