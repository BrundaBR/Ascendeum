#imports modules 
import random
import pandas as pd

class Board:
    def __init__(self,size=9):
        self.size = size
        self.snakes = {
            8:3,
            4:2,
        }
        self.ladder = {
            3:7,
            5:8
        }
    
    def get_position(self, pos:int):
        # check if new position encounters snakes or ladder
        if pos in self.snakes:
            return self.snakes[pos]
        elif pos in self.ladder:
            return self.ladder[pos]
        return pos

class Dice:
    @staticmethod
    def roll():
        # return random number from 1 to 6 similar to dice
        return random.randint(1,6)

class Players:
    def __init__(self,number):
        self.number = number
        self.position = 0
        self.win_status = False
        self.roll_dice_history =[]
        self.position_history = []
    
    def next_move(self, new_pos: int, board:Board):
        # dice should not go beyond end number
        if self.position + new_pos > board.size:
            return self.position
        self.position_history.append(new_pos) 

        new_pos = self.position + new_pos
        
        new_pos = board.get_position(new_pos)
        self.position = new_pos
        # Player wins: new position has reached end
        if new_pos == board.size:
            self.win_status = True
        return new_pos 
        

class Snake_Ladder:
    def __init__(self,players):
        self.players = players
        self.round = 0
        self.board = Board()
        self.result = []
        self.previous_position = []


    def play(self):
        while True:
            #increment round details
            self.round+=1

            for player in self.players:
                # dice roll
                dice_roll_1 = Dice.roll()
                # dice_roll_2 = Dice.roll()
                
                player.roll_dice_history.append(dice_roll_1)
                new_position_res = dice_roll_1 

                # check with new position with move in player class
                next_move=player.next_move(new_position_res,self.board)

                for i in self.players:
                    if i.position_history!=[]:
                        val = i.position_history[-1]
                        if i!=player and  next_move == val :
                            i.position = 0


                # store it in list
                win_stat = "Win!" if player.win_status else "Lost"

                position_history = player.position_history
                previous_position_history = (','.join([str(i) for i in position_history]))

                dice_roll = player.roll_dice_history
                previous_dice_history = (','.join([str(i) for i in dice_roll]))

                self.result.append({
                    "Player_Number": player.number,
                    "Dice Roll History": previous_dice_history,
                    "Position History":  previous_position_history,
                    "Result" : win_stat
                })

                if player.win_status:
                    return

def main():
    players=["1","2","3"]
    players = [Players(i) for i in players]
    game = Snake_Ladder(players)
    game.play()

    # Display result in table format
    df = pd.DataFrame(game.result)
    print(df)

if __name__== "__main__":
    print("Starting Snake and Ladder--")
    main()