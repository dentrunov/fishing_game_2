import pygame as pg

from random import randint, choice, uniform
import time, os, keyboard

from settings import *


class Fish:
    '''рыбы'''
    def __init__(self, name, min_size=1, max_size=10000, frequency=50, heaviness=50):
        self.name = name
        self.__min_size = min_size
        self.__max_size = max_size
        self.__size = randint(self.__min_size, self.__max_size)
        self.frequency = frequency #частотность рыбы в водоеме??? в процентах, меньше - чаще
        self.heaviness = heaviness #сложность вылавливания рыбы, меньше - сложнее, нужно для схода при поклевке

    @property
    def size(self):
        return self.__size

    def eat(self):
        pass

    def __del__(self):
        print('Рыба сброшена')
        pass

    def __repr__(self):
        return f"Рыба {self.name}, {self.size}"

fish_names = [
    ['Карась', 100, 1000, 100, 70],
    ['Карп', 300, 3000, 300, 30]
    ]

fish_classes = [Fish('Карась', 100, 1000, 100), Fish('Карп', 300, 3000, 300)]

class Rod(pg.sprite.Sprite):
    '''удилища'''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = 'popl'
        self.name = 'Поплавочка'
        self.lenght = 300
        self.weight = 4
        self.active = False #доступна к использованию ??
        self.usable = False #заброшена
        self.down = True #подсеченная - False
        # self.image = pg.Surface('rod.png')
        self.image = pg.transform.scale(pg.image.load('rod.png'), (10, 400))
        self.pop = Pop()
        self.coords = [-1000, 1000]
        self.new_fish = None
    
    def get(self, mouse_x, mouse_y):
        """ Достаем удилище """
        # self.active = not(self.active)
        if not (self.active):
            self.active = True
            self.coords = [mouse_x, 350]
            self.pop.image = pg.transform.scale(self.pop.image, (10, 40))

        else:
            self.active = self.usable = False
            self.coords = [-10000, -10000]
            # rod_x = -10000
            # rod_y = -10000
            # pop_x, pop_y = (-10000, -10000)
        return self.coords

    def put(self, mouse_x, mouse_y):
        '''заброс'''
        if not self.usable:
            self.usable = True
        # mouse_y -= 35
        if mouse_x < 5: mouse_x = 5
        if mouse_x > WIDTH - 5: mouse_x = WIDTH - 5
        if mouse_y < MAX_HEIGHT: mouse_y = MAX_HEIGHT
        if mouse_y > HEIGHT - 5: mouse_y = HEIGHT - 5
        if mouse_x < WIDTH - 200:
            self.coords[0] = mouse_x + 50
        else:
            self.coords[0] = mouse_x - 50

        self.pop.coords = [mouse_x, mouse_y]
        return self.pop.coords, self.coords
        
    def get_fish(self):
        """Подсечка"""
        self.pop.transform((10,10))
        self.pop.coords[1] += 10
        self.down = False

    def push(self, fish):
        if self.active:
            if randint((0,1)):
                self.fish = fish
                print(fish.name)
            else:
                print('Сорвалась')

class Pop(pg.sprite.Sprite):
    '''поплавки'''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.active = False
        self.usable = False
        # self.image = pg.Surface('rod.png')
        self.image = pg.image.load('pop.png')
        self.coords = [-1000, 1000]
        self.size = (10, 20)
        self.__last_move = 1
    
    @property
    def last_move(self):
        return self.__last_move
    
    @last_move.setter
    def last_move(self, x):
        self.__last_move = x
        print(222, self.__last_move)

    def transform(self, x):
        self.size = x
        # self.last_move = 1
        self.coords[0] += self.size[1] - x[1] 
        self.image = pg.transform.scale(self.image, x)



class River:
    pass


class Player:
    pass


def print_pressed_keys(e):
    print(e, e.event_type, e.name)


if __name__ == '__main__':
    rod = Rod()
    while True:
        f = choice(fish_classes)
        f.size =randint(f.min_size, f.max_size)
        chance = [0] * f.frequency + [1]
        if choice(chance):
            print(f.name, f.size, 'клюёт')
        else:
            continue

        #os.system('CLS')
