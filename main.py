import pygame
from player import *
from colors import *
from coin import *
from random import randrange
from point_text import *
import pandas as pd

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Inital things
pygame.init()
background = BLACK

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

clock = pygame.time.Clock()
screen = pygame.display.set_mode(((SCREEN_WIDTH, SCREEN_HEIGHT)))

player = Player()
font = pygame.font.SysFont(None, 24)

# Player/Game Properties
boost = False
inflate = False
coins_ct = 0
points = 0
time = 100 # seconds
start_ticks=pygame.time.get_ticks()

coins = []
point_texts = []

timer_interval = 1000 
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event , timer_interval)

endTimer = 60000  # seconds * 1000
end_event = pygame.USEREVENT + 2
pygame.time.set_timer(end_event, endTimer)

start_ticks=pygame.time.get_ticks()

def end():

    print("Game Ended")
    print("Coins: ", coins_ct)
    print("Points: ", points)

    # read scores and get high score
    game_data = pd.read_csv('game_scores.csv')
    df = pd.DataFrame(game_data)
    max_value = df['Score'].max()

    end_text = font.render("END", True, GRAY)
    screen.blit(end_text, (SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 - 50))

    # display highscore
    highscore_text = font.render("Current Highscore: " + str(max_value), True, GRAY)
    screen.blit(highscore_text, (SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 - 30))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(event)
            if pygame.joystick.Joystick(0).get_button(3):
                
                new_data = {'Score': [points], 'Coins':[coins_ct], 'Seconds': [60]}
                df = df.append(pd.DataFrame(new_data), ignore_index=True)
                df.to_csv('game_scores.csv', index=False)
                pygame.quit()

while True:

    # Seconds passed till game started
    seconds = (pygame.time.get_ticks()-start_ticks)/1000

    # Update Text on Screen
    x_pos_text = font.render("X: " + str(player.player.x), True, GRAY)
    y_pos_text = font.render("Y: " + str(player.player.y), True, GRAY)
    boost_text = font.render("Boost: " + str(boost), True, GRAY)
    coins_text = font.render("Coins: " + str(coins_ct), True, GRAY)
    points_text = font.render("Points: " + str(points), True, GRAY)
    seconds_text = font.render("Seconds: " + str(seconds), True, GRAY)
    
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == end_event:
            end()
        # Button Presses
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
            if pygame.joystick.Joystick(0).get_button(1):
                print("Turn on Boost")
                boost = True
            if pygame.joystick.Joystick(0).get_button(2):
                print("Inflate")
                inflate = True
        # Button Releases
        if event.type == pygame.JOYBUTTONUP:
            print(event)
            if not pygame.joystick.Joystick(0).get_button(1):
                print("Turn off Boost")
                boost = False
            if not pygame.joystick.Joystick(0).get_button(2):
                print("Deflate")
                inflate = False
        # Sticks Moved
        # if event.type == pygame.JOYAXISMOTION:
        #     print(event)
        # Timer Event
        if event.type == timer_event:
            coins.append(Coin(randrange(50 , SCREEN_WIDTH - 50), randrange(50 , SCREEN_HEIGHT - 50), randrange(100, 300), randrange(5, 40)))
            print("New coin appeard")

    # Set Speed and direction based on Left Stick
    x_speed = round(pygame.joystick.Joystick(0).get_axis(0) * (5 if boost else 1) * (0.7 if inflate else 1))
    y_speed = round(pygame.joystick.Joystick(0).get_axis(1) * (5 if boost else 1) * (0.7 if inflate else 1))

    if boost and inflate:
        x_speed = 0
        y_speed = 0

    player.move(x_speed, y_speed)

    if inflate:
        player.inflate()
    else:
        player.deflate()

    # Draw things
    screen.fill(background)
    player.draw(screen)

    # Handle Coins
    for coin in coins:
        coin.timer = coin.timer - 1

        if not coin.collected:
            coin.draw(screen)
        if coin.timer < 50:
            coin.change_color("orange")
        if coin.timer < 25:
            coin.change_color("red")
        if coin.timer < 0:
            coins.remove(coin)
            del coin
            continue

        # Collect coin whe colliding
        if pygame.Rect.colliderect(player.player, coin.coin):
            coin.collect()
            coins_ct = coins_ct + 1
            points = points + coin.points

            # Display added points
            if coin.timer < 50:
                points = points + 5
                point_texts.append(PointText(coin.coin.x, coin.coin.y - 12, font, 5, "orange"))

            if coin.timer < 25:
                points = points + 10
                point_texts.append(PointText(coin.coin.x, coin.coin.y - 24, font, 10, "red"))

            point_texts.append(PointText(coin.coin.x, coin.coin.y, font, coin.points))

            coins.remove(coin)
            del coin
            continue
    
    # draw point text
    for p_text in point_texts:
        p_text.timer = p_text.timer -1
        p_text.draw(screen)
        if p_text.timer < 0:
            point_texts.remove(p_text)
            del p_text
            continue
    
    # Draw Texts
    RIGHT_BOUND = 150
    screen.blit(x_pos_text, (20, 20))
    screen.blit(y_pos_text, (20, 40))
    screen.blit(boost_text, (SCREEN_WIDTH - RIGHT_BOUND, 20))
    screen.blit(coins_text, (SCREEN_WIDTH - RIGHT_BOUND, 40))
    screen.blit(points_text, (SCREEN_WIDTH - RIGHT_BOUND, 60))
    screen.blit(seconds_text, (SCREEN_WIDTH/2 - 50, 20))

    pygame.display.update()
    clock.tick(180)
        
print("Coins: ", coins)
pygame.quit()