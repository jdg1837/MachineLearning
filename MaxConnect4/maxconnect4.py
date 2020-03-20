#!/usr/bin/env python

# Written by Juan Diego Gonzalez
# based on code by Chris Conly and Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import MaxConnect4Minimax
import sys

def oneMoveGame(currentGame, outfile, depth):
    #update input state
    print 'Game state before move:'
    updateGameBoard(currentGame)

    #make a move
    currentGame = MaxConnect4Minimax.aiPlay(currentGame, depth)

    #update final state
    print 'Game state after move:'
    printToFile(currentGame, outfile)
    updateGameBoard(currentGame)

def interactiveGame(currentGame, computer_next, depth):
    while(True):
        if computer_next:
            updateGameBoard(currentGame)
            currentGame = MaxConnect4Minimax.aiPlay(currentGame, depth)
            printToFile(currentGame, "computer.txt")
            computer_next = not computer_next
        
        else:
            updateGameBoard(currentGame)
            currentGame = MaxConnect4Minimax.humanPlay(currentGame)
            printToFile(currentGame, "human.txt")
            computer_next = not computer_next

def updateGameBoard(currentGame):    
    currentGame.printGameBoard()
    currentGame.getScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    
    if currentGame.isTerminal():    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'  
        sys.exit(0)

def printToFile(currentGame, outfile):
    try:
        currentGame.gameFile = open(outfile, 'w')
    except:
        sys.exit('Error opening output file.')
    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]
    depth = int(argv[4])

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = MaxConnect4Minimax.MaxConnect4Game.maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.max_player = currentGame.currentTurn

    currentGame.gameFile.close()

    print '\nMaxConnect-4 game\n'

    if game_mode == 'interactive':
        computer_next = True
        if not argv[3] == 'computer-next':
            computer_next = False
            currentGame.max_player = (currentGame.max_player % 2) + 1
        interactiveGame(currentGame, computer_next, depth) # Be sure to pass whatever else you need from the command line

    else: # game_mode == 'one-move'
        outfile = argv[3]
        oneMoveGame(currentGame, outfile, depth) # Be sure to pass any other arguments from the command line you might need.

if __name__ == '__main__':
    main(sys.argv)