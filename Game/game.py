


class Game:

    def __init__(self, id):
        self.player_1 = False
        self.player_2 = False
        self.ready = False
        self.id = id 
        self.team = [None, None]


    def connected(self):
        return self.ready
    
    def left(self):
        return self.player_1 and self.player_2

    def team(self):
        pass 
