from game import *

# import pygame as pg
# import time
# настройки окна
WIDTH = 1200
HEIGHT = 800
MAX_HEIGHT = 300
FPS = 30
COLOR = (240, 240, 240)
BLACK = (0, 0, 0)
pg.init()

background = pg.image.load("back.jpg")
background = pg.transform.scale(background, (WIDTH, HEIGHT-50))

clock = pg.time.Clock()

screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(COLOR)
pg.display.set_caption('Рыбалка')

#удочка
rod = Rod()
pop = pg.image.load('pop.png')
pop_x, pop_y = (-10000, -10000)
rod_x = -10000
rod_y = -10000

#группируем спрайты
all_sprites = pg.sprite.Group()
# all_sprites.add(rod, pop)

def set_text(txt):
    '''функция подготовки текста'''
    text_field = f1.render(txt, True, BLACK)
    screen.blit(text_field, (10, HEIGHT - 40))

#подготовка текста
f1 = pg.font.SysFont('arial', 20)
set_text('Начало игры')

def fish_generate():
    ''' генерация клева рыбы '''
    chance = [0] * 100 + [1]
    if choice(chance):
        f = Fish(*choice(fish_names))
        print(f'{f.name} {f.size} г. клюёт в {time.time()}')
        set_text(f'{f.name} {f.size} г. клюёт в {time.time()}')
        return f
    return False

def pop_move(y, fish, last_move, fish_activity_time):
    '''анимация поклевки'''
    if rod.down:
        #генерируем паузу поклевки
        if time.time() - fish_activity_time > uniform(0.0, 2.0):
            # просчитываем прекращение клёва
            if not choice([1] * fish.heaviness * 10 + [0]):
                global new_fish
                new_fish = 0
                print('Перестала клевать')
                set_text('Перестала клевать')
                return y, last_move, fish_activity_time

            if last_move == 1:
                last_move = 0
                y += 2
            else:
                last_move = 1
                y -= 2
            if y < MAX_HEIGHT: y = MAX_HEIGHT
            if y > HEIGHT - 5: y = HEIGHT - 5
            fish_activity_time = time.time()

    return y, last_move, fish_activity_time


#игровой цикл
game_over = True
new_fish = False
while game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = False
            break
        if event.type == pg.KEYDOWN:
            # достаем и убираем удочку
            if event.key == pg.K_1:
                if not (rod.active):
                    rod.active = rod.usable = True
                    rod.down = True
                    rod_x = WIDTH // 2
                    rod_y = 300
                    rod.pop.image = pg.transform.scale(rod.pop.image, (10, 40))

                else:
                    rod.active = rod.usable = False
                    rod.down = True
                    rod_x = -10000
                    rod_y = -10000
                    pop_x, pop_y = (-10000, -10000)

            if event.key == pg.K_SPACE:
                if rod.active and rod.down:
                    rod.pop.image = pg.transform.scale(rod.pop.image, (10, 10))
                    rod.down = False
        if event.type == pg.MOUSEBUTTONDOWN:
            # заброс удочки
            if event.button == 1:
                if rod.active:
                    pop_x, pop_y = event.pos
                    if pop_x < 5: pop_x = 5
                    if pop_x > WIDTH - 5: pop_x = WIDTH - 5
                    if pop_y < MAX_HEIGHT: pop_y = MAX_HEIGHT
                    if pop_y > HEIGHT - 5: pop_y = HEIGHT - 5
                    if pop_x < WIDTH - 200:
                        rod_x = pop_x + 50
                    else:
                        rod_x = pop_x  - 50

    #поклевка
    if all((rod.down, rod.active, rod.usable)):
        if not new_fish:
            new_fish = fish_generate()
            last_move = 1
            fish_activity_time = time.time()
        else:
            pop_move__, last_move, fish_activity_time = pop_move(pop_y, new_fish, last_move, fish_activity_time)
            pop_y = pop_move__

    screen.blit(background, (0, 0))  # отрисовка фона
    screen.blit(rod.image, (rod_x, rod_y))  # отрисовка удочки
    screen.blit(rod.pop.image, (pop_x, pop_y))  # отрисовка поплавка

    # all_sprites.draw(screen)
    pg.display.update()
    clock.tick(FPS)

print('Конец')
pg.quit()