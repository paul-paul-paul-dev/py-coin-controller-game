import pygame

class Coin(object):
    
    def __init__(self, x_pos, y_pos, timer, size):
        self.coin = pygame.rect.Rect((x_pos,y_pos,size,size))
        self.color = "yellow"
        self.collected = False
        self.timer = timer
        self.points = ((41-size) * 2) + round((301-timer) / 10) 

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.coin)

    def change_color(self, color_str):
        self.color = color_str

    def collect(self):
        self.collected = True
        print("Coin has been collected")

    def __del__(self):
      print ("Coin gets destroyed")
