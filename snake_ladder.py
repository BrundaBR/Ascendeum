#imports modules 
import random
import pandas as pd

'''
3x3
9(0,2)8(1,2)(2,2)7
6(0,1)5(1,1)4(2,1)
1(0,0)2(1,0)3(2,0)
'''

class Board:
    def __init__(self,size=9):
        self.size = size
        self.n = int(self.size ** 0.5)
        self.snakes = {
            # 8:3,
            # 4:2,
        }
        self.ladder = {
            # 3:7,
            # 5:8
        }
    
    def get_position(self, pos:int)->int:
        # check if new position encounters snakes or ladder
        if pos in self.snakes:
            return self.snakes[pos]
        elif pos in self.ladder:
            return self.ladder[pos]
        return pos
    
    #Get cordinates of a position
    def cordinate_pos(self, pos):
        if pos == 0:
            return (-1,-1)
        col = (pos -1) // self.n
        row = (pos -1) % self.n
        if  col % 2 == 1:
            row = self.n - 1- row
        return (row,col)

class Dice:
    @staticmethod
    def roll()->int:
        # return random number from 1 to 6 similar to dice
        return random.randint(1,6)

class Players:
    def __init__(self,number):
        self.number = number
        self.position = 0
        self.win_status = False
        self.roll_dice_history =[]
        self.position_history = []
        self.cordinates = []
    
    def next_move(self, new_pos: int, board:Board)->int:
        # dice should not go beyond end number
        if self.position + new_pos > board.size:
            return self.position
        
        self.roll_dice_history.append(new_pos)
        new_pos = self.position + new_pos
        new_pos = board.get_position(new_pos)
        self.position = new_pos
        self.position_history.append(self.position) 
        self.cordinates.append(board.cordinate_pos(self.position))
        
        # Player wins: new position has reached end
        if new_pos == board.size:
            self.win_status = True
        return new_pos 

@staticmethod
def check_repeat(pos,players,curr_player)->None:
     for i in players:
        if i.position_history!=[]:
            val = i.position_history[-1]
            if i!=curr_player and  pos == val :
                i.position = 0
                # i.cordinates.pop(0)
                i.cordinates=[(-1,-1)]

class Snake_Ladder:
    def __init__(self,players):
        self.players = players
        self.round = 0
        self.board = Board()
        self.result = []
        self.previous_position = []

    def play(self)->None:
        while True:
            #increment round details
            self.round+=1

            for player in self.players:
                dice_roll_1 = Dice.roll()

                # check with new position with move in player class
                next_move=player.next_move(dice_roll_1,self.board)

                #Check  if player already exist in position
                check_repeat(next_move, self.players,player)

                self.result.append({
                    "Player_Number": player.number,
                    "Dice Roll History": (','.join([str(i) for i in player.roll_dice_history])),
                    "Position History":  (','.join([str(i) for i in player.position_history])),
                    "Cordinates History" : ''.join([ f"({r},{c})" for r,c in player.cordinates]),
                    "Result" : "Winner!" if player.win_status else "Lost"
                })

                if player.win_status:
                    return

def main():
    players=["p1","p2","p3"]
    players = [Players(i) for i in players]
    game = Snake_Ladder(players)
    game.play()

    # Display result in table format
    df = pd.DataFrame(game.result)
    print(df)

if __name__== "__main__":
    print("Starting Snake and Ladder:")
    main()