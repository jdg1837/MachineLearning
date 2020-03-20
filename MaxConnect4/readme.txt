Name: Juan Diego Gonzalez German
ID: 1001401837
Language: Python 2.4

Run:
python maxconnect4.py interactive [input_file] [computer-next/human-next] [depth]
OR
python maxconnect4 one-move [input_file] [output_file] [depth]

Code Structure:

The code is divided in three files: maxconnect4.py, MaxConnect4Minimax.py, and MaxConnect4Game.py.
MaxConnect4Game.py simply contains the maxConnect4Game class, which is basically the template for all gamestate objects, 
and contains the functions related to those. This class contains functions to test if a gamestate is a terminal one or not (aka, if the board is full),
count pieces, print the board either to the screen or to the file, and calculate a final score, or an approximate desirability of a state through an 
evaluation function (See the Evaluation file for detailed information)
The main driver of the game is the code on the maxconnect4.py. This is the file that includes the main function that is called when the program is ran.


The main function initializes the current gamestate as given by the board on the input file, and depending of the mode, it calls the oneMoveGame or the interactiveGame functions. 
The former simply prints the current board to the player, makes a move, and then prints the new gamestate both to the screen and to the specified output file. 
The interactive game alternates between computer and human, asking the user to make a move, or making a move itself. Both functions make calls to the updateGameBoard function, 
in the same file. This one simply calls the function in the maxConnect4Game class to print to file, checks piece count and score, printing the latter. 
The update function also calls the isTerminal function to check if the board is full. If it is, the game is over and the program closes. 
The oneMoveGame or the interactiveGame functions also call the printToFile function, which opens the output file, calls the actual function that prints to that file in the Game class, 
and then closes the file.

The MaxConnect4Minimax module handles moves in the game. The only functions in it called from the outside are humanPlay and aiPlay. 
The former simply asks for the user to select what column to play, checks for it to be valid, and calls the play function for it. 
The aiPlay initializes and calls the minimax function, which then goes into minPlay and maxPlay functions of the Minimax algorithm, with alpha-beta pruning all in the same file. 
The minimax algorithm compares values for all possible moves of the current state and selects the best one. 
The moves possible moves are found by the getMoves, which connects a future gamestate with a column to play in a tuple. 
he minimax algorithm jumps between MinPlay and MaxPlay until the max depth is reached, at which point either the final score or an eval utility is returned
