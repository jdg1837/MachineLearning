def calculateScore(gameBoard, player, actualScore):
    playerScore = 0

    for row in gameBoard:
        for i in range (4):
            playerScore += checkSequence(row[i:4+i], player, actualScore)
    
    for col in range(7):
        for h in range (3):
            vertical = []
            vertical.append(gameBoard[0+h][col])
            vertical.append(gameBoard[1+h][col])
            vertical.append(gameBoard[2+h][col])
            vertical.append(gameBoard[3+h][col])
            playerScore += checkSequence(vertical, player, actualScore)

    diagonals = createDiagonals(gameBoard)

    for diagonal in diagonals:
        playerScore += checkSequence(diagonal, player, actualScore)

    return playerScore

def createDiagonals(gameBoard):
    diagonals = []
    diagonals.append([gameBoard[2][0], gameBoard[3][1], gameBoard[4][2], gameBoard[5][3]])
    diagonals.append([gameBoard[1][0], gameBoard[2][1], gameBoard[3][2], gameBoard[4][3]])
    diagonals.append([gameBoard[2][1], gameBoard[3][2], gameBoard[4][3], gameBoard[5][4]])
    diagonals.append([gameBoard[0][0], gameBoard[1][1], gameBoard[2][2], gameBoard[3][3]])
    diagonals.append([gameBoard[1][1], gameBoard[2][2], gameBoard[3][3], gameBoard[4][4]])
    diagonals.append([gameBoard[2][2], gameBoard[3][3], gameBoard[4][4], gameBoard[5][5]])
    diagonals.append([gameBoard[0][1], gameBoard[1][2], gameBoard[2][3], gameBoard[3][4]])
    diagonals.append([gameBoard[1][2], gameBoard[2][3], gameBoard[3][4], gameBoard[4][5]])
    diagonals.append([gameBoard[2][3], gameBoard[3][4], gameBoard[4][5], gameBoard[5][6]])
    diagonals.append([gameBoard[0][2], gameBoard[1][3], gameBoard[2][4], gameBoard[3][5]])
    diagonals.append([gameBoard[1][3], gameBoard[2][4], gameBoard[3][5], gameBoard[4][6]])
    diagonals.append([gameBoard[0][3], gameBoard[1][4], gameBoard[2][5], gameBoard[3][6]])

    diagonals.append([gameBoard[0][3], gameBoard[1][2], gameBoard[2][1], gameBoard[3][0]])
    diagonals.append([gameBoard[0][4], gameBoard[1][3], gameBoard[2][2], gameBoard[3][1]])
    diagonals.append([gameBoard[1][3], gameBoard[2][2], gameBoard[3][1], gameBoard[4][0]])
    diagonals.append([gameBoard[0][5], gameBoard[1][4], gameBoard[2][3], gameBoard[3][2]])
    diagonals.append([gameBoard[1][4], gameBoard[2][3], gameBoard[3][2], gameBoard[4][1]])
    diagonals.append([gameBoard[2][3], gameBoard[3][2], gameBoard[4][1], gameBoard[5][0]])
    diagonals.append([gameBoard[0][6], gameBoard[1][5], gameBoard[2][4], gameBoard[3][3]])
    diagonals.append([gameBoard[1][5], gameBoard[2][4], gameBoard[3][3], gameBoard[4][2]])
    diagonals.append([gameBoard[2][4], gameBoard[3][3], gameBoard[4][2], gameBoard[5][1]])
    diagonals.append([gameBoard[1][6], gameBoard[2][5], gameBoard[3][4], gameBoard[4][3]])
    diagonals.append([gameBoard[2][5], gameBoard[3][4], gameBoard[4][3], gameBoard[5][2]])
    diagonals.append([gameBoard[2][6], gameBoard[3][5], gameBoard[4][4], gameBoard[5][3]])

    return diagonals

def checkSequence(seq, player, actualScore):
    opponent = (player % 2) + 1
    if opponent in seq:
        return 0

    player_count = 0
    for piece in seq:
        if piece == player:
            player_count += 1
    if player_count == 4:
        return 1
    if actualScore:
        return 0
    elif player_count == 3:
        return 0.25
    elif player_count == 2:
        return 0.05
    elif player_count == 1:
        return 0.01
    else:
        return 0