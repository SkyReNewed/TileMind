import numpy as np
import random
import os

def initializeBoard():
    # Create a 4x4 board with two random tiles.
    board = np.zeros((4, 4), dtype=int)
    addNewTile(board)
    addNewTile(board)
    return board

def addNewTile(board):
    # Add a 2 (90% chance) or 4 (10% chance) to a random empty cell.
    emptyCells = list(zip(*np.where(board == 0)))
    if emptyCells:
        row, col = random.choice(emptyCells)
        board[row][col] = 2 if random.random() < 0.9 else 4

def displayBoard(board, score):
    # this function displays the board in a formatted way.
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 33)
    print("            2048 GAME")
    print("=" * 33)
    print(f"  Score: {score}")
    print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
    for row in board:
        print("|", end="")
        for cell in row:
            if cell == 0:
                print("       |", end="")
            else:
                print(f"{cell:^7}|", end="")
        print()
        print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
    print("\nControls: W(Up) S(Down) A(Left) D(Right) Q(Quit)")

def compress(board):
    # Slide all non-zero tiles to the left.
    newBoard = np.zeros((4, 4), dtype=int)
    for i in range(4):
        pos = 0
        for j in range(4):
            if board[i][j] != 0:
                newBoard[i][pos] = board[i][j]
                pos += 1
    return newBoard

def merge(board):
    # Merge adjacent equal tiles (after compression).
    score = 0
    for i in range(4):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                board[i][j] *= 2
                board[i][j + 1] = 0
                score += board[i][j]
    return board, score

def moveLeft(board):
    # Perform a left move.
    newBoard = compress(board)
    newBoard, score = merge(newBoard)
    # Compress again after merging to remove empty spaces
    newBoard = compress(newBoard)
    return newBoard, score

def moveRight(board):
    # Flip the left and right side of board and move left
    flipped = np.fliplr(board)
    newBoard, score = moveLeft(flipped)
    return np.fliplr(newBoard), score

def moveUp(board):
    # Rotate the board and move left
    transposed = board.T
    newBoard, score = moveLeft(transposed)
    return newBoard.T, score

def moveDown(board):
    # Rotate the board and move right (flip and move left)
    transposed = board.T
    newBoard, score = moveRight(transposed)
    return newBoard.T, score

def isGameOver(board):
    # If there's any empty cell, game is not over
    if 0 in board:
        return False
    # Check for possible merges horizontally
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1]:
                return False
    # Check for possible merges vertically
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i + 1][j]:
                return False
    return True

def hasWon(board):
    # Win Condition
    return 2048 in board

def playGame():
    # Main Loop
    board = initializeBoard()
    score = 0
    won = False

    moves = {
        'w': moveUp,
        's': moveDown,
        'a': moveLeft,
        'd': moveRight
    }

    while True:
        displayBoard(board, score)

        if hasWon(board) and not won:
            print("\nCongratulations! You reached 2048!")
            print("You can continue playing or press Q to quit.")
            won = True

        if isGameOver(board):
            print("\nGame Over! No more moves possible.")
            print(f"   Final Score: {score}")
            break

        # Get player input
        move = input("\nYour move: ").lower().strip()

        if move == 'q':
            print(f"\nFinal Score: {score}")
            break

        if move not in moves:
            print("Invalid input! Use W/A/S/D to move, Q to quit.")
            continue

        # Execute the move
        newBoard, moveScore = moves[move](board)

        # Check if the board actually changed
        if np.array_equal(board, newBoard):
            continue  # Invalid move, nothing changed

        board = newBoard
        score += moveScore
        addNewTile(board)

if __name__ == "__main__":
    playGame()
