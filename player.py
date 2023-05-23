import pygame 

display_rect = pygame.rect.Rect((0,0,800,800))

class Player(object):

    def __init__(self):
        self.player = pygame.rect.Rect((300,400,10,10))
        self.color = "white"

    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed,y_speed))
        self.player.clamp_ip(display_rect)

    def inflate(self):
        if self.player.width < 25 and self.player.height < 25:
            self.player = self.player.inflate(2,2)

    def deflate(self):
        if self.player.width > 10 and self.player.height > 10:
            self.player = self.player.inflate(-2,-2)

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)