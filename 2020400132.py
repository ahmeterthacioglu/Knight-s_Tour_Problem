
import random
import time
import sys
def is_valid_move(board, x, y):
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1
def find_valid_start():
    start_x = random.randint(0, n - 1)
    start_y = random.randint(0, n - 1)
    return start_x, start_y
def knight_tour(p):
    board = [[-1 for i in range(n)] for i in range(n)]
    x, y = find_valid_start()
    board[x][y] = 0
    total_squares = 1
    tour_steps = [(x, y)]

    while True:
        valid_moves = []
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(board, new_x, new_y):
                valid_moves.append((new_x, new_y))

        if not valid_moves:
            break

        # Choose a move randomly from valid moves
        x, y = random.choice(valid_moves)

        board[x][y] = total_squares
        tour_steps.append((x, y))
        total_squares += 1

        if total_squares > n * n * p:
            break
    if(total_squares >= n*n*p):
        result = "Successful"
    else:
        result = "Unsuccessful"
    tour_length = total_squares
    return result, tour_length, tour_steps, board

def knight_tour_backtracking(p, k):
    board = [[-1 for i in range(n)] for i in range(n)]
    x, y = find_valid_start()
    board[x][y] = 0
    total_squares = 1
    tour_steps = [(x, y)]

    for i in range(k):
        valid_moves = []
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(board, new_x, new_y):
                valid_moves.append((new_x, new_y))

        if not valid_moves:
            break

        # Choose the move with the fewest available future moves (Warnsdorff's Rule)
        #valid_moves.sort(key=lambda move: sum(1 for dx, dy in moves if is_valid_move(board, move[0] + dx, move[1] + dy)))
        #x, y = valid_moves[0]
        x, y = random.choice(valid_moves)
        tour_steps.append((x,y))
        board[x][y] = total_squares
        total_squares += 1


    # Apply backtracking to find a successful tour
    success = backtracking(board, tour_steps, total_squares, n * n * p, k)

    tour_length = total_squares if success else -1
    result = "Successful" if success else "Unsuccessful"
    return result, tour_length, board,

def backtracking(board, tour_steps, total_squares, target_squares,k):

    if total_squares >= target_squares:
        return True

    x, y = tour_steps[-1]

    valid_moves = []
    for dx, dy in moves:
        new_x, new_y = x + dx, y + dy
        if is_valid_move(board, new_x, new_y):
            valid_moves.append((new_x, new_y))

    # Sort valid moves by Warnsdorff's Rule (ascending order of available future moves)
    valid_moves.sort(key=lambda move: sum(1 for dx, dy in moves if is_valid_move(board, move[0] + dx, move[1] + dy)))

    for move in valid_moves:
        new_x, new_y = move
        board[new_x][new_y] = total_squares
        tour_steps.append((new_x, new_y))
        total_squares += 1

        if backtracking(board, tour_steps, total_squares, target_squares,k):
            return True

        # Backtrack
        if len(tour_steps) > k:
            x,y = tour_steps.pop()
            board[x][y] = -1

            total_squares -= 1

    return False

n = 8  # Board size
moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
         (-2, -1), (-1, -2), (1, -2), (2, -1)]
def main():
    if sys.argv[1] == "part1":
        start_time = time.time()

        for p in [0.7, 0.8, 0.85]:
            results = []
            successful_tours = 0
            total_trials = 100000

            for count in range(1, total_trials + 1):
                result, length, tour_steps, board = knight_tour(p)
                if result == "Successful":
                    successful_tours += 1
                i = 0
                for step in tour_steps:
                    if (i == 0):
                        results.append(f"Run {count}: starting from {step}")
                        i = 1
                    else:
                        results.append(f"Stepping into {step}")
                results.append(f"{result} - Tour length: {length}")
                for i in range(n):
                    row = ' '.join(str(board[i][j]) if (i, j) in tour_steps else '-1' for j in range(n))
                    results.append(row)
                results.append('')

            probability = successful_tours / total_trials

            print(f"LasVegas Algorithm With p = {p}")
            print(f"Number of successful tours: {successful_tours} ")
            print(f"Number of trials: {total_trials}")
            print(f"Probability of a successful tour: {probability}")
            file_name = f"results_{p}.txt"
            with open(file_name, 'w') as file:
                for line in results:
                    file.write(line + '\n')
            end_time = time.time()
            elapsed_time = end_time - start_time
            print()
            #print(elapsed_time)

    if sys.argv[1] == "part2":

        for p in [0.7,0.8,0.85]:
            for k in [0,2,3]:
                start_time = time.time()
                results = []
                successful_tours = 0
                total_trials = 100000

                for count in range(1, total_trials + 1):
                    result, length, board = knight_tour_backtracking(p, k)
                    if result == "Successful":
                        successful_tours += 1
                probability = successful_tours / total_trials
                print(f"--- p = {p} ---")
                print(f"LasVegas Algorithm With p = {p}, k = {k}")
                print(f"Number of successful tours: {successful_tours} Number of trials: {total_trials}")
                print(f"Probability of a successful tour: {probability}")

                end_time = time.time()
                elapsed_time = end_time - start_time
                print()
                #print(elapsed_time)

if __name__ == "__main__":
    main()
