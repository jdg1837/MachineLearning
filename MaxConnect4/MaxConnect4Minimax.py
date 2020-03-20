import MaxConnect4Game
import copy
import math
import sys

def humanPlay(currentGame):
    while(True):
        try:
            col = input('Please chose a column to play: ')
        except:
            print("Invalid input, please try again")
            continue
        if col == 'q':
            print("Aborting....")
            sys.exit(0)
        if col not in range (1,8):
            print("Choice not valid, must be between 1 and 7")
            continue
        result = currentGame.playPiece(col-1)
        if not result:
            print("That column is already full! Please try again")
            continue
        else:
            return currentGame

def aiPlay(currentGame, max_depth):
    column_choice = minimaxDecision(currentGame, max_depth)
    print('\n\nmove %d: Player %d, column %d\n' % (currentGame.pieceCount, currentGame.currentTurn, column_choice+1))
    currentGame.playPiece(column_choice)
    return currentGame

def minimaxDecision(currentGame, max_depth):
    moves = getMoves(currentGame)
    util = -float('Inf')
    choice = -1
    for game_move in moves:
        current_util = minValue(game_move[0], -float('Inf'), float('Inf'), max_depth, 1)
        if(current_util > util):
            util = current_util
            choice = game_move[1]
    return choice

def maxValue(gameState, alpha, beta, max_depth, depth):
    if gameState.isTerminal():
        return gameState.getScore()
    if depth >= max_depth:
        return gameState.getUtility()

    v = -float('inf')
    moves = getMoves(gameState)
    for game_move in moves:
        min_result = minValue(game_move[0], alpha, beta, max_depth, depth + 1)
        v = max(v, min_result)
        if v >= beta:
             return v
        alpha = max(alpha, v)
    return v

def minValue(gameState, alpha, beta, max_depth, depth):
    if gameState.isTerminal():
        return gameState.getScore()
    if depth >= max_depth:
        return gameState.getUtility()
    
    v = float('inf')
    moves = getMoves(gameState)
    for game_move in moves:
        max_result = maxValue(game_move[0], alpha, beta, max_depth, depth + 1)
        v = min(v, max_result)
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def getMoves(gameState):
    moves = []
    for col in range (4):
        game_move = copy.deepcopy(gameState)
        result = game_move.playPiece(3-col)
        if result:
            moves.append((game_move,3-col))

        if col == 0:
            continue

        game_move = copy.deepcopy(gameState)
        result = game_move.playPiece(3+col)
        if result:
            moves.append((game_move,3+col))       
    return moves