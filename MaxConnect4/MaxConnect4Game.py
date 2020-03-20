#!/usr/bin/env python

# Written by Juan Diego Gonzalez
# based on code by Chris Conly and Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import MaxConnect4Board

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.max_player = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None

    def isTerminal(self):
        self.checkPieceCount()
        return self.pieceCount == 42

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.currentTurn = (self.currentTurn % 2) + 1
                    self.pieceCount += 1
                    return 1

    def getScore(self):
        self.player1Score = MaxConnect4Board.calculateScore(self.gameBoard, 1, True)
        self.player2Score = MaxConnect4Board.calculateScore(self.gameBoard, 2, True)

        if self.max_player == 1: 
            return self.player1Score - self.player2Score
        else:
            return self.player2Score - self.player1Score

    def getUtility(self):
        player1Utility = MaxConnect4Board.calculateScore(self.gameBoard, 1, False)
        player2Utility = MaxConnect4Board.calculateScore(self.gameBoard, 2, False)

        if self.max_player == 1: 
            return player1Utility - player2Utility
        else:
            return player2Utility - player1Utility