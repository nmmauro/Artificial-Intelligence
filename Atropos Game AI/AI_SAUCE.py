import sys
import random
# print to stderr for debugging purposes
# remove all debugging statements before submitting your code
    
def next_moves(lastPlay):
    """define a function to find all possible moves, if all of them are colored, 
    consider the board as empty since we can choose random move.
    @type lastPlay: list
    @rtype list[list],boolean
    """
    move_1 = [lastPlay[1]+1]+[lastPlay[2]-1]+[lastPlay[3]] # upper left
    move_2 = [lastPlay[1]]+[lastPlay[2]-1]+[lastPlay[3]+1] # left
    move_3 = [lastPlay[1]+1]+[lastPlay[2]+1]+[lastPlay[3]-1] # upper right
    move_4 = [lastPlay[1]]+[lastPlay[2]+1]+[lastPlay[3]-1] # right
    move_5 = [lastPlay[1]-1]+[lastPlay[2]]+[lastPlay[3]+1] # lower left
    move_6 = [lastPlay[1]-1]+[lastPlay[2]+1]+[lastPlay[3]] # lower right
    if (lastPlay[1] == 1): # bottom line
        move_5 = [lastPlay[1]-1]+[lastPlay[2]-1]+[lastPlay[3]] # lower left
        move_6 = [lastPlay[1]-1]+[lastPlay[2]]+[lastPlay[3]-1] # lower right
    result = []
    counter = 0
    _empty = False
    if (check_color(move_1) != 0):
        result += [move_1]
        counter += 1
    if (check_color(move_2) != 0):
        result += [move_2]
        counter += 1
    if (check_color(move_3) != 0):
        result += [move_3]
        counter += 1
    if (check_color(move_4) != 0):
        result += [move_4]
        counter += 1
    if (check_color(move_5) != 0):
        result += [move_5]
        counter += 1
    if (check_color(move_6) != 0):
        result += [move_6]
        counter += 1
    if (counter == 6): # all of the adjacent moves is colored
        _empty = True
    return result,_empty
    
def check_color(move):
    """define a function to check the color in the board given [x,y,z]
    @type move: list
    @rtype int
    """
    sys.stderr.write(str(move));
    return int(board[size+1-move[0]][move[1]])

def checker(move):
    """define a function to check whether a move will end the game
    @type move: list
    @rtype boolean
    """
    sys.stderr.write(str(move)+"\n");
    if (check_color(move[1:]) != 0):
        return True
    if (move[0] + int(board[size+1-move[1]][move[2]-1]) + int(board[size-move[1]][move[2]-1]) == 6 and move[0] != int(board[size+1-move[1]][move[2]-1])):
        return True # upper left triangle
    if (move[0] + int(board[size+1-move[1]][move[2]-1]) + int(board[size+2-move[1]][move[2]]) == 6 and move[0] != int(board[size+1-move[1]][move[2]-1])):
        return True # lower left triangle
    if (move[0] + int(board[size+1-move[1]][move[2]+1]) + int(board[size-move[1]][move[2]]) == 6 and move[0] != int(board[size+1-move[1]][move[2]+1])):
        return True # upper right triangle
    if (move[1] == 1):
        if (move[0] + int(board[size+1-move[1]][move[2]+1]) + int(board[size+2-move[1]][move[2]]) == 6 and move[0] != int(board[size+1-move[1]][move[2]+1])):
            return True # lower right triangle
    else:
        if (move[0] + int(board[size+1-move[1]][move[2]+1]) + int(board[size+2-move[1]][move[2]+1]) == 6 and move[0] != int(board[size+1-move[1]][move[2]+1])):
            return True # lower right triangle
    return False

#parse the input string, i.e., argv[1]
index = sys.argv[1].find("LastPlay:");
# msg = "Given board " + sys.argv[1] + "\n";
# sys.stderr.write(msg);
board = sys.argv[1][:index] # board as string
board = board.replace('[','').split(']')[:-1] # convert board into list
lastPlay = sys.argv[1][index+9:]; # lastPlay as String
size = len(board)-2 # size of the board
empty = False
if (lastPlay == "null"):
    empty = True # check whether the board is empty

# When the board is not empty, convert lastPlay into a list: [color, x, y, z]
lastPlay_list = [0] * 4
sys.stderr.write(str(empty)+"\n");
if (not empty):
    lastPlay_list[0] = int(lastPlay[1])
    lastPlay_list[1] = int(lastPlay[3])
    lastPlay_list[2] = int(lastPlay[5])
    lastPlay_list[3] = int(lastPlay[7])
    empty = next_moves(lastPlay_list)[1]
    
# When the board is empty, make a random move without losing the game
if (empty):
    move = [0] * 4
    move[0] = random.randint(1,3)
    move[1] = random.randint(1,size)
    move[2] = random.randint(1,size+1-move[1])
    move[3] = size + 2 - move[1] - move[2]

    while (checker(move)):
        move[0] = random.randint(1,3)
        move[1] = random.randint(1,size)
        move[2] = random.randint(1,size+1-move[1])
        move[3] = size + 2 - move[1] - move[2]
    
    sys.stdout.write("("+str(move[0])+","+str(move[1])+","+str(move[2])+","+str(move[3])+")");

#perform intelligent search to determine the next move

#print to stdout for AtroposGame
if (not empty):
    move = []
    move += [random.randint(1,3)]
    possible_moves = next_moves(lastPlay_list)[0]
    random_number = random.randint(0,len(possible_moves))
    move += possible_moves[random_number]
    sys.stdout.write("("+str(move[0])+","+str(move[1])+","+str(move[2])+","+str(move[3])+")");
# As you can see Zook's algorithm is not very intelligent. He 
# will be disqualified.

