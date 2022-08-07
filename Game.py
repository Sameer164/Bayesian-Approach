import matplotlib
from math import comb
matplotlib.use('module://pygame_matplotlib.backend_pygame')
import matplotlib.pyplot as plt
import pygame
import scipy
import sys
import pylab
import json
from scipy import special
pygame.font.init()
import numpy as np
WIDTH, HEIGHT = 1200,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLIP THE COIN")
WHITE = (255, 255, 255)
FPS = 25
TABLE = pygame.image.load("table.webp.webp")
BORDER = pygame.Rect(WIDTH/2 - 10, 0, 5, HEIGHT)
BLACK = (0,0,0)
NORMAL_IMAGE = pygame.image.load("heads.png")
NORMAL = pygame.transform.scale(NORMAL_IMAGE, (100,100))
TAILS_IMAGE = pygame.image.load("tails.png")
TAILS = pygame.transform.scale(TAILS_IMAGE, (100,100))
SIDE_IMAGE = pygame.image.load("coin_side.jpg")
SIDE = pygame.transform.scale(SIDE_IMAGE, (100,100))
POS = 1
ALL = [TAILS, NORMAL, SIDE]
NUM_HEADS = 0
GAME_NUM = 1
TRIALS = 0
TOTAL_HEADS = 0
BIASED_PROB_HEAD = 0.8
PREV_GAMES = None
PREV_HEADS = None
POINTS_FONT = pygame.font.SysFont('comicsans', 30)
POINTS_FONT2 = pygame.font.SysFont('comicsans', 15)
ALPHA = 5
BETA = 1
Rs = np.linspace(0,1,num=100,endpoint=True)
RS = Rs





#0 is a tail
#1 is a head

def draw_coin():
    WIN.blit(ALL[POS%3], (970, 360))
        


def display_points():

    if not PREV_GAMES and not PREV_HEADS:


        points = POINTS_FONT.render(f"Curr Game# {GAME_NUM} HEADS# {NUM_HEADS}",1,BLACK)
        WIN.blit(points, (WIDTH-points.get_width()-10, 10))
    else:

        points0 = POINTS_FONT.render(f"Prev Games# {PREV_GAMES} HEADS# {PREV_HEADS}",1,BLACK)
        points = POINTS_FONT.render(f"Curr Game# {GAME_NUM} HEADS# {NUM_HEADS}",1,BLACK)
        WIN.blit(points0, (WIDTH-points0.get_width()-10, 10))
        WIN.blit(points, (WIDTH-points.get_width()-10, 10+points.get_height()))
        




def beta_distribution():
    global ALPHA, BETA, TRIALS, TOTAL_HEADS, Rs
    gamma_funcs = special.gamma(ALPHA + BETA + TRIALS) / (special.gamma(ALPHA + TOTAL_HEADS) * special.gamma(BETA + TRIALS - TOTAL_HEADS))
    return (Rs ** (ALPHA + TOTAL_HEADS - 1)) * ((1-Rs)**(BETA + TRIALS - TOTAL_HEADS - 1)) * gamma_funcs

def plot_distribution():
    fig, axes = plt.subplots(1, 1,)
    axes.plot(Rs, beta_distribution(), color='green', label='test')
    axes.set_title("Probability of Head Dist.")
    fig.canvas.draw()
    WIN.blit(fig, (0,50))
    WIN.blit(POINTS_FONT2.render("Probability of head",1,BLACK), (250, 500))








def update():
    WIN.fill(WHITE)
    plot_distribution()
    display_points()
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(TABLE, (750,300))
    draw_coin()
    pygame.display.update()






def main():
    global GAME_NUM, TRIALS, NUM_HEADS, TOTAL_HEADS, BIASED_PROB_HEAD, POS, PREV_GAMES, PREV_HEADS
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            POS += 1
        # else:
        #     TRIALS += 1
        #     if TRIALS % 10 == 0:
        #         PREV_GAMES = GAME_NUM
        #         PREV_HEADS = TOTAL_HEADS
        #         GAME_NUM += 1
        #         NUM_HEADS = 0
        #     SIDE = np.random.binomial(1, BIASED_PROB_HEAD)
        #     NUM_HEADS += 1
        #     TOTAL_HEADS += 1
        #     POS = SIDE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYUP:
                if TRIALS % 10 == 0 and TRIALS != 0:
                    PREV_GAMES = GAME_NUM
                    PREV_HEADS = TOTAL_HEADS
                    GAME_NUM += 1
                    NUM_HEADS = 0
                TRIALS += 1
                SIDE = np.random.binomial(1, BIASED_PROB_HEAD)
                NUM_HEADS += SIDE
                TOTAL_HEADS += SIDE
                POS = SIDE
            


        update()
    pygame.quit()
    obj={"TRIALS": TRIALS, "TOTAL_HEADS": TOTAL_HEADS, "PREV_GAMES": PREV_GAMES, "NUM_HEADS": NUM_HEADS}
    with open("sample.json", "w") as outfile:
        json.dump(obj, outfile)
    sys.exit()
    




main()
