def display_board(game_board):
        print(f"|{game_board[20]} | {game_board[21]} | {game_board[22]} | {game_board[23]} |{game_board[24]} | ")
        print(f"|---------|")
        print(f"|{game_board[15]} | {game_board[16]} | {game_board[17]} | {game_board[18]} | {game_board[19]} ")
        print(f"|---------|")
        print(f"|{game_board[10]} | {game_board[11]} | {game_board[12]} |{game_board[13]} | {game_board[14]} ")
        print(f"|---------|")
        print(f"|{game_board[5]}| {game_board[6]} | {game_board[7]} | {game_board[8]} |{game_board[9]} ")
        print(f"|---------|")
        print(f"|{game_board[0]} | {game_board[1]} | {game_board[2]} | {game_board[3]} | {game_board[4]}")

def user_choice(game_board):
        choice=''
        acceptable_range=range(1,26)
        within_range = False
        error_message="sorry, enter a valid board position (1-25):"

        while choice.isdigit()== False or within_range==False:

            choice=input(f"{player_turn}, please select a board position (1-25):")
            if choice.isdigit()==False:
                print(error_message)
            elif choice.isdigit() == True:
                if int(choice) not in acceptable_range or game_board[int(choice)-1] !='':
                    print(error_message)
                    within_range=False
                else:
                    within_range=True

        return int(choice)  
    

def resume_play_choice():
        choice=''
        acceptable_range=['Y','N']

        while choice not in  acceptable_range:

            choice = input("play again (Y orN)? ") 

            if choice not in acceptable_range:
                print("Sorry, please enter a valid selection.")

        if choice == 'Y':
            return True
        else:
            return False
        
def toggle_player_turn(player_turn):
        if player_turn =="PlayerX":
            return "PlayerY"
        else:
            return "PlayerX"
        
def check_win(game_game):
        winning_combos =[[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19],[20,21,22,23,24] ]

        for combo in winning_combos:
            if game_board[combo[0] ] =="X" and   game_board[combo[1]] =="X" and game_board[combo[2]] =="X":
                return True
            
            if game_board[combo[0]] =="O" and game_board[combo[1]] =="O" and game_board[combo[2]]=="O":
                return True 
        else:
            return False


from IPython.display import clear_output


game_board = ['','','','','','','','','','','','','','','',
              '','','','','','','','','','']
game_on=True
player_map={"PlayerX":"X", "PlayerY":"O"}
player_turn ="PlayerX"

while game_on:
    clear_output(wait=False)
    display_board(game_board)
    choice= user_choice(game_board)
    game_board[choice-1]= player_map[player_turn]
    win = check_win(game_board)
    if win == True:
        clear_output(wait = False)
        display_board(game_board)
        print(f"{Player_turn} wins!")
        game_on= resume_play_choice()
        if game_on:
            game_board= ['','','','','','','','','','','','','','','',
              '','','','','','','','','','']
    else:
        player_turn= toggle_player_turn(player_turn)
