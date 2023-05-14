import pygame as pg

from random import randint, choice, uniform
import time, os, keyboard
class Fish:
    '''рыбы'''
    def __init__(self, name, min_size=1, max_size=10000, frequency=50, heaviness=50):
        self.name = name
        self.min_size = min_size
        self.max_size = max_size
        self.size = randint(self.min_size, self.max_size)
        self.frequency = frequency #частотность рыбы в водоеме??? в процентах, меньше - чаще
        self.heaviness = heaviness #сложность вылавливания рыбы, меньше - сложнее, нужно для схода при поклевке

    def eat(self):
        pass

    def __del__(self):
        print('Рыба сброшена')
        pass

fish_names = [['Карась', 100, 1000, 100, 70], ['Карп', 300, 3000, 300, 30]]

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
        self.image = pg.image.load('rod.png')
        self.pop = Pop()

    def put(self):
        '''заброс'''
        active = True

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
        chance = [0] * f.frequency + [1]
        if choice(chance):
            print(f.name, f.set_size(randint(f.min_size, f.max_size)), 'клюёт')
        else:
            continue

        #os.system('CLS')
