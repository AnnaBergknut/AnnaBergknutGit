import random

class PlayRoom:
    """  """
    def __init__(self):
        """ My attributes """
        self._game = None
        self._players = []
        self._winner = None

    def set_game(self, whatGame):
        """ Choose what game to play. ship of fools are with when we call this function """ 
        self._game = whatGame        

    def add_player(self, name):
        """ adds player to a list """
        self._players.append(name)

    def reset_score(self):
        """ turn the score to 0 for every player """
        for i in self._players:
            i.reset_score()

    def play_round(self):
        """ play a round for eatch player """
        for player in self._players:
            player.play_turn(self._game)

    def game_finished(self):
        """ check if any of the players have won and call on print_score and print_winner """
        for player in self._players: 
            if player.current_score() >= self._game.winning_score:
                self._player.print_winner()
                self.player.print_score()
                return True
            else:
                return False
                              
    def print_score(self):
        """ print the score """
        for i in self._players:
            print(" The score was", i.current_score())

    def print_winner(self):
        """ Determin who won and print name"""
        print(self._winner, "won the game!!!")

class Player:
    """ A Player """
    def __init__(self, name):
        """ My attributes """
        self.name = name
        self.score = 0
        
    def __str__(self):
        """ make the objeckt return the name not the path """
        return self.name

    def current_score(self):
        """ return score """
        return self.score

    def reset_score(self):
        """ after the game is done reset the score """
        self.score = 0
        
    def play_turn(self, whatGame):
        """ add to the score and start the turn """
        self.score += whatGame.turn()

class ShipOfFoolsGame:
    """ the game logic """
    def __init__(self):
        """ My attributes """
        howManyDice = 5
        self._cup = DiceCup(howManyDice)
        self.winning_score = 50
        

    def turn(self):
        """ do a turn for one player"""
        has_ship = False
        has_captain = False
        has_mate = False
        crew = 0
        number = 0

        for i in range(3):
            
            for index, die in enumerate(self._cup._dice):
                die.roll()
                if not self._cup._isBanked[index]: # sätt else if på de andra
                    number = self._cup.value(index)
                
                if has_ship == False and number == 6:
                    has_ship == True
                    self._cup.bank(die)
                
                if has_ship and not has_captain and number == 5:
                    has_captain == True
                    self._cup.bank(die)
                    
                if has_captain and not has_mate and number == 4:
                    has_mate == True
                    self._cup.bank(die)
                    
                if has_mate and number > 3:
                    self._cup.bank(die)
                    
        if has_mate:
            for index, dice in self._cup._dice:
                crew += self._cup.value(index)
                print(crew)
        return crew - 15
                               
        """
        if has_ship and has_captain and has_mate:
            crew := sum of all dice - 15 
        """

class DiceCup:
    """ The cup with dice, handle the objeckts """
    def __init__(self, howManyDice):
        """ My attributes and create amount of dice needed """
        self._isBanked = []
        self._dice = []
        for i in range(howManyDice):
            self._dice.append(Die())
            self._isBanked.append(False)

    def value(self, index):
        """ return the value of the dice with that index"""
        die = self._dice[index]
        return die.get_value()

    def bank(self, index):
        """ bank the index that you sent in """
        self._isBanked[index] == True

    def is_banked(self, index):
        """ return the value of the index in _isbanked """
        return self._isBanked[index]

    def release(self,index):
        """ take a index and turn that one to false in _isBancked """
        self._isBanked[index] == False

    def release_all(self):
        """ make all of the index in _isbanked flase """
        for i in self._isBanked:
            self._isBanked[i] == False

    def roll(self):
        """ for every die in _dice call on roll in die to get a new number """
        for die in self._dice:
            die.roll()

class Die:
    """ Handle one objekt namely the die that we can roll in order to get a value """
    def __init__(self):
        """ My attributes """
        self._value = 0

    def get_value(self):
        """ Return the curent value"""
        return self._value

    def roll(self):
        """ Roll a new number for this die """
        self._value = random.randint(1,6)


if __name__ == "__main__":
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame())
    room.add_player(Player('Nora'))
    room.add_player(Player('Selman'))
    room.reset_score() 
    while not room.game_finished():
        room.play_round()
        room.print_score()
    room.print_winner()