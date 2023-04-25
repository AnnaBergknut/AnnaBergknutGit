import random
import DiceCup

"""

   
   det första man ska göra är att dicecup skapar tärningar. samt att ship of fools skapar dicecup. när den ena dör så dör alla som har skapas av dem.
   börja med att göra ship of fools.
   
   copen skapar fem olika objekt med 
   
   när jag modelerar ska jag tänka på att metoderna ska både vara vad objektet används samt vad andra objekt ska använda det till.
   
   man kan ha en poblic metod för att komma år namnet i players för tt displaya namn på winer i playroom
   
   ship of fool vet hur mång tärningar den har
   
   finns tid på freag med hjälp.
    
   
    
"""

 
class ShipOfFoolsGame:
    winning_score = 50  
    _cup = "DiceCup"
    dice = 5
    
    def __init__(room):
        room.dicecup = room.DiceCup()
    
    def turn():
        """ do a turn for 1 player"""
        has_ship = False
        has_captain = False
        has_mate = False

        # This will be the sum of the remaining dice, i.e., the score.
        crew = 0

        # Repeat three times
        
      
       
        """
        for _ in range(3):
            roll unbanked dice # call on rool in dicecup
            if not has_ship and a dice is 6: # kollaar om det fiins en 6 i listan med en forlop först
                bank it
                has_ship = True
            if has_ship and not has_captain and a dice is 5: # kollar om det finns en 5 baserat på att vi har en 6
                # A ship but not a captain is banked
                bank it
                has_captain = True
            if has_captain and not has_mate and a dice is 4: saammma som innan men med 5 istället för 6.
                # A ship and captain but not a mate is banked
                bank it
                has_mate = True
        
            if has_ship and has_captain and has_mate:
                # Now we got all needed dice, and can bank the ones we like to save.
                bank all unbanked dice > 3

        # If we have a ship, captain and mate (sum 15), 
        # calculate the sum of the two remaining.
        if has_ship and has_captain and has_mate:
            crew := sum of all dice - 15 """
        
        # startar en runda 
    
     

 
def main():
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame())
    room.add_player(Player('Nora'))
    room.add_player(Player('Selman'))
    room.reset_scores()
    while not room.game_finished():
        room.play_round()
        room.print_scores()
    room.print_winner()
    
    
if __name__ == "__main__":
    main()
