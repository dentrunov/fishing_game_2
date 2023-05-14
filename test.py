import pygame as pg
import sys

WIDTH = 1200
HEIGHT = 800
FPS = 30
COLOR = (240, 64, 128)
pg.init()

background = pg.image.load("back.jpg")

clock = pg.time.Clock()

screen = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption('Рыбалка')

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill((150, 150, 150))