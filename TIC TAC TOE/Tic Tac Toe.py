import random
import time

print('Welcome to Tic Tac Toe!')

def player_input():
    player1,player2 =('','')
    while player1!='O' and player1!='X':
        player1=(input('Player 1, please select "O" or "X":')).upper()
    if player1 == 'X':
        return ('X','O')
    else:
        return ('O','X')
    

def choose_first():
    turn=random.randint(1,2)
    if turn==1:
        print ('Player 1 starts first')
        return True
    else:
        print ('Player 2 starts first')
        return False


def display_board(board):
    print('   |  '+' |   ')
    print(' '+board[7] +' | '+board[8]+' | ' +board[9])
    print('---|--'+'-|---')
    print(' '+board[4] +' | '+board[5]+' | ' +board[6])
    print('---|--'+'-|---')
    print(' '+board[1] +' | '+board[2]+' | ' +board[3])
    print('   |  '+' |   ')
    
    
def space_check(board, position):
    return board[position]==' '   
    
def player_choice(board):   
    while True:
        position=int(input('Please specify position:'))
        space_check(board, position)
    
        if space_check(board, position) is True:
        #print ("{} {}".format("You chose position:", position))
            return position
            break
        else:
            print('You cannot cheat in this game:)')
            continue
        
def place_marker(board, marker, position):
    board[position]=marker
    
def full_board_check(board):
    return ' ' in board

def win_check(board, mark):
    if (board[1]==board[2]==board[3] == mark) or \
        (board[4]==board[5]==board[6]== mark) or \
        (board[7]==board[8]==board[9]== mark) or \
        (board[1]==board[4]==board[7]== mark) or \
        (board[3]==board[6]==board[9]== mark) or \
        (board[1]==board[5]==board[9]== mark) or \
        (board[3]==board[5]==board[7]== mark):
        return True
    
def replay():
    decision=input('Would you like to play again? Y/N:')
    if decision.upper() == 'Y':
        return True
    else:
        return False   
    
    
    
while True:
    board = ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    player1,player2=player_input()
    whofirst=choose_first()
    game_on = True
    
    while game_on:
        print('\n'*100) 
        display_board(board)
        
        if whofirst==True:  #first player
            print('Player 1')
            position=player_choice(board)
            place_marker(board,player1,position)
            if win_check(board, player1):
                print('\n'*100)
                print('Congrats Player 1 !')
                break
            else:
                whofirst=False
        
        elif whofirst==False:
            print('Player 2')
            position=player_choice(board)
            place_marker(board,player2,position)
            if win_check(board, player2)==True:
                print('\n'*100)
                print('Congrats Player 2 !')
                break
            else:
                whofirst=True

        if not full_board_check(board):     #False = no place anymore
            print('\n'*100)
            print ('Nobody won')
            break      
        else:
            pass
            
        
    display_board(board)       
    if replay()==True:
        pass
    else:
        print('Goodbye')
        time.sleep(2)
        break
