import heapq

# Hàm để tính h(n), khoảng cách Mahattan
def heuristic(state, goal_state):
    n = len(state)
    h = 0
    for i in range(n):
        for j in range(n):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, n)
                h += abs(x - i) + abs(y - j)
    return h

# Hàm để tạo trạng thái con sau mỗi bước di chuyển
def get_neighbors(state):
    n = len(state)
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:
                x, y = i, j
                break
    
    neighbors = []
    
    # Di chuyển lên (N)
    if x > 0:
        new_state = [row[:] for row in state]
        new_state[x][y], new_state[x - 1][y] = new_state[x - 1][y], new_state[x][y]
        neighbors.append(('N', new_state))
    
    # Di chuyển xuống (S)
    if x < n - 1:
        new_state = [row[:] for row in state]
        new_state[x][y], new_state[x + 1][y] = new_state[x + 1][y], new_state[x][y]
        neighbors.append(('S', new_state))
    
    # Di chuyển sang trái (W)
    if y > 0:
        new_state = [row[:] for row in state]
        new_state[x][y], new_state[x][y - 1] = new_state[x][y - 1], new_state[x][y]
        neighbors.append(('W', new_state))
    
    # Di chuyển sang phải (E)
    if y < n - 1:
        new_state = [row[:] for row in state]
        new_state[x][y], new_state[x][y + 1] = new_state[x][y + 1], new_state[x][y]
        neighbors.append(('E', new_state))
    
    return neighbors

# Hàm chính để giải N puzzle bằng A*
def solve_n_puzzle(n, initial_state):
    goal_state = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    goal_state[n - 1][n - 1] = 0
    
    open_list = [(0, '', initial_state)]
    closed_set = set()
    
    while open_list:
        _, path, state = heapq.heappop(open_list)
        if state == goal_state:
            return len(path), path
        closed_set.add(tuple(map(tuple, state)))
        
        for move, neighbor_state in get_neighbors(state):
            if tuple(map(tuple, neighbor_state)) not in closed_set:
                g = len(path) + 1
                h = heuristic(neighbor_state, goal_state)
                f = g + h
                heapq.heappush(open_list, (f, path + move, neighbor_state))
    
    return -1, ''  

# Tạo puzzle
def create(n):
    puzzle = []
    for _ in range(n):
        row = []
        for _ in range(n):
            while True:
                try:
                    num = int(input())
                    if num < 0 or num >= n * n:
                        raise ValueError("Số không hợp lệ. Hãy nhập lại.")
                    if num in row:
                        raise ValueError("Số đã tồn tại trong hàng. Hãy nhập lại.")
                    row.append(num)
                    break
                except ValueError as e:
                    print(e)
        puzzle.append(row)
    return puzzle

n = int(input("Nhập kích thước n: "))
print('Nhập câu đố: ')
initial_state = create(n)

min_moves, solution_path = solve_n_puzzle(n, initial_state)
print("Số lượt di chuyển ít nhất:", min_moves)
print("Chuỗi các lượt di chuyển:", solution_path)
