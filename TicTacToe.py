"""
Lucas' Tic-Tac-Toe game V1

Three game modes avaliable
--------------------------
play_1v1() - play againsts your friends if you have any
play_ai() - play against an ai which a child could beat
play_unwinnable() - play against an ai which if you beat I will persoanlly give you £100
"""
import numpy as np
import time

def board(player, cur_board, pos):
    """
    Function which controls the addition of characters to the board
    ---------------------------------------------------------------
    Inputs
    ------
    player - The symbol of the current player
    cur_board - The current state of the tic-tac-toe board
    pos - The position which the player has chosen to add their character
    ---------------------------------------------------------------------
    Returns
    -------
    new_board - The current board inputted with the new character added in a given position
    """
    
    # dictionary which converts positions into indexes of the board
    positions = {"1":30,
                 "2":34,
                 "3":38,
                 "4":86,
                 "5":90,
                 "6":94,
                 "7":142,
                 "8":146,
                 "9":150
        }
    # verify that the input is valid
    while pos not in positions:
        pos = input("That is not a valid position! Try again: ")
    # loop to verify if current position chose is taken
    while cur_board[positions[pos]] != " ":
        pos = input("That position is already taken! Try again: ")
        while pos not in positions:
            pos = input("That is not a valid position! Try again: ")
    # creates a new board with inputted position
    new_board = cur_board[:positions[pos]]+player+cur_board[positions[pos]+1:]
    return new_board

def has_won(player, cur_board):
    """
    Function to verify if a player has won
    --------------------------------------
    Inputs
    ------
    player - The curent player's character
    cur_board - The current state of the tic-tac-toe board
    Returns
    -------
    None, 0- If no player has won
    player, 1 - If the current player has won
    """
    
    # converts the positions on the board into a 3x3 matrix to easily check
    matrix = np.array([[cur_board[30], cur_board[34], cur_board[38]],
              [cur_board[86], cur_board[90], cur_board[94]],
              [cur_board[142], cur_board[146], cur_board[150]]])
    # checks all rows and columns
    for i in range(3):
        if list(matrix[i]).count(player) == 3:
            return player, 1
        if list(matrix[0:3, i]).count(player) == 3:
            return player, 1
    # checks the diagonals
    if list(np.diagonal(matrix)).count(player) == 3:
        return player, 1
    if list(np.diagonal(np.fliplr(matrix))).count(player) == 3:
        return player, 1
    return None, 0

def ai(player, cur_board):
    """
    Function for the ai to play the optimal move using the recursive minimax algorithm
    ----------------------------------------------------------------------------------
    Inputs
    ------
    player - current player (will always be "O")
    cur_board - the current state of the board
    Returns
    -------
    best_move - The best move for the ai so that is always wins or ties
    """
    positions = {"1":30,
                "2":34,
                "3":38,
                "4":86,
                "5":90,
                "6":94,
                "7":142,
                "8":146,
                "9":150
       }
    board = [cur_board[30], cur_board[34], cur_board[38],
              cur_board[86], cur_board[90], cur_board[94],
              cur_board[142], cur_board[146], cur_board[150]]
    empty = [i+1 for i, x in enumerate(board) if x == " "] # generate an array of all the empty indices
    
    # checks if winner and end recursion
    if has_won("X", cur_board)[1] == 1:
        result = {"index": None, "score": -10}
        return result
    elif has_won("O", cur_board)[1] == 1:
        result = {"index": None, "score": 10}
        return result
    elif not empty:
        result = {"index": None, "score": 0}
        return result
    
    # recursion begins here
    moves = []
    for i in empty:
        move = {"index": None, "score": None}
        move["index"] = i
        new_board = cur_board[:positions[str(i)]]+player+cur_board[positions[str(i)]+1:]
        
        if player == "O":
            result = ai("X", new_board)
        else:
            result = ai("O", new_board)
        
        move["score"] = result["score"]
        moves.append(move)
    
    if player == "O":
        best_score = -10000
        for i in moves:
            if i["score"] > best_score:
                best_score = i["score"]
                best_move = i
    else:
        best_score = 10000
        for i in moves:
            if i["score"] < best_score:
                best_score = i["score"]
                best_move = i
    
    return best_move


def play_1v1():
    """
    Main function to play TicTacToe versus another player
    -------------------------------
    Inputs
    ------
    None
    Returns
    -------
    If player X has won
    If player O has won
    If no one has won
    """
    
    # initialise constants
    winner = None # The winner (initially None)
    turns = 0 # current turn
    won = 0 # 0 if no one has won, 1 if someone has won
    # The empty board
    cur_board = "|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|"
    while won != 1:
        # if board is full and no one has won then game over
        if turns == 9:
            print(f"\n{cur_board}\n")
            return print("Nobody wins. Game over")
        # player X's turn
        if turns % 2 == 0:
            turns += 1
            pos = str(input(f"{cur_board}\n\nIt's Player X's Turn (1-9): "))
            # adds new character to the board
            cur_board = board("X", cur_board, pos)
            # verify if player has won
            winner, won = has_won("X", cur_board)
        # player O's turn
        elif turns % 2 != 0:
            turns += 1
            # adds new character to the board
            pos = str(input(f"{cur_board}\n\nIt's Player O's Turn (1-9): "))
            # verify is player has one
            cur_board = board("O", cur_board, pos)
            winner, won = has_won("O", cur_board)
        # if board is full and no one has won then game over
    return print(f"\n{cur_board}\n\nGame over. Player {winner} wins!")

def play_unwinnable():
    """
    Main function to play TicTacToe versus an unwinnable ai
    -------------------------------
    Inputs
    ------
    None
    Returns
    -------
    If player X has won
    If player O has won
    If no one has won
    """
    
    # initialise constants
    winner = None # The winner (initially None)
    turns = 0 # current turn
    won = 0 # 0 if no one has won, 1 if someone has won
    # The empty board
    cur_board = "|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|"
    while won != 1:
        # if board is full and no one has won then game over
        if turns == 9:
            print(f"\n{cur_board}\n")
            return print("Nobody wins. Game over")
        # player X's turn
        if turns % 2 == 0:
            turns += 1
            pos = str(input(f"{cur_board}\n\nIt's your Turn (1-9): "))
            # adds new character to the board
            cur_board = board("X", cur_board, pos)
            # verify if player has won
            winner, won = has_won("X", cur_board)
        # ai's turn
        elif turns % 2 != 0:
            turns += 1
            # adds new character to the board
            print(f"{cur_board}\n\nComputer thinking... ")
            pos = str(ai("O", cur_board)["index"])
            time.sleep(1.5) # add time to simulate the computer "thinking" for that authentic robot feeling
            # verify is player has won
            cur_board = board("O", cur_board, pos)
            winner, won = has_won("O", cur_board)
        # if board is full and no one has won then game over
    return print(f"\n{cur_board}\n\nGame over. Player {winner} wins!")

def play_ai():
    """
    Main function to play TicTacToe against an ai you can beat
    -------------------------------
    Inputs
    ------
    None
    Returns
    -------
    If player X has won
    If player O has won
    If no one has won
    """
    
    # initialise constants
    winner = None # The winner (initially None)
    turns = 0 # current turn
    won = 0 # 0 if no one has won, 1 if someone has won
    # The empty board
    cur_board = "|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|\n|   |   |   |\n|   |   |   |\n|   |   |   |\n|---|---|---|"
    while won != 1:
        # if board is full and no one has won then game over
        if turns == 9:
            print(f"\n{cur_board}\n")
            return print("Nobody wins. Game over")
        # player X's turn
        if turns % 2 == 0:
            turns += 1
            pos = str(input(f"{cur_board}\n\nIt's your Turn (1-9): "))
            # adds new character to the board
            cur_board = board("X", cur_board, pos)
            # verify if player has won
            winner, won = has_won("X", cur_board)
        # ai's turn
        elif turns % 2 != 0:
            turns += 1
            print(f"{cur_board}\n\nComputer thinking... ")
            ai_board = [cur_board[30], cur_board[34], cur_board[38],
                     cur_board[86], cur_board[90], cur_board[94],
                     cur_board[142], cur_board[146], cur_board[150]]
            empty = [i+1 for i, x in enumerate(ai_board) if x == " "] # generate an array of all the empty indices
            # adds new character to the board
            pos = str(np.random.choice(empty))
            time.sleep(1.5)
            # verify is player has one
            cur_board = board("O", cur_board, pos)
            winner, won = has_won("O", cur_board)
        # if board is full and no one has won then game over
    return print(f"\n{cur_board}\n\nGame over. Player {winner} wins!")

if __name__=="__main__":
    play_unwinnable()
    


    
