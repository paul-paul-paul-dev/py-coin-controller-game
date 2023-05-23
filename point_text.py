import pygame

class PointText(object):
    
    def __init__(self, x_pos, y_pos, font, points, color = "yellow"):
        self.text = font.render("+" + str(points), True, color)
        self.timer = 75
        self.x = x_pos
        self.y = y_pos

    def draw(self, game_screen):
        game_screen.blit(self.text, (self.x, self.y))

    def __del__(self):
      print ("Text gets destroyed")