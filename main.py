from game import *
from settings import WIDTH, HEIGHT, MAX_HEIGHT, FPS, COLOR_FILL, BLACK

from datetime import datetime


pg.init()

background = pg.image.load("back.jpg")
background = pg.transform.scale(background, (WIDTH, HEIGHT-50))

clock = pg.time.Clock()

screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(COLOR_FILL)
pg.display.set_caption('Рыбалка')

#удочка
rod = Rod()
pop = pg.image.load('pop.png')

#группируем спрайты
all_sprites = pg.sprite.Group()
# all_sprites.add(rod, pop)

def set_text(txt):
    '''функция подготовки текста'''
    screen.fill(COLOR_FILL)
    text_field = f1.render(txt, True, BLACK)
    screen.blit(text_field, (10, HEIGHT - 40))

#подготовка текста
f1 = pg.font.SysFont('arial', 20)
set_text('Начало игры')

def fish_generate():
    ''' генерация клева рыбы '''
    # chance = [0] * 100 + [1]
    chance = [0] * 1000 + [1]
    if choice(chance):
        f = Fish(*choice(fish_names))
        rod.pop.image = pg.transform.scale(rod.pop.image, (10, 20))  
        # rod.pop.coords = [rod.pop.coords[0], rod.pop.coords[1] - 20]
        tm = datetime.now()
        print(f'{f.name} {f.size} г. клюёт в {tm}')
        set_text(f'{f.name} {f.size} г. клюёт в {tm}')
        return f
    return False

def pop_move(y, fish, last_move, fish_activity_time):
    '''анимация поклевки'''
    if rod.down:
        #генерируем паузу поклевки
        if time.time() - fish_activity_time > uniform(0.0, 2.0):
            # просчитываем прекращение клёва
            if not choice([1] * fish.heaviness * 10 + [0]):
                # переделать на ООП
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
                rod.get(*pg.mouse.get_pos())

            if event.key == pg.K_SPACE:
                #подсечка TODO
                if rod.active and rod.down:
                    rod.pop.image = pg.transform.scale(rod.pop.image, (10, 10))
                    rod.down = False

        if event.type == pg.MOUSEBUTTONDOWN:
            # заброс удочки
            if event.button == 1:
                if rod.active and rod.down:
                    rod.put(*event.pos)

    # поклевка
    # if all((rod.down, rod.active, rod.usable)):
    #     if not new_fish:
    #         new_fish = fish_generate() 
    #         rod_x, rod_y = rod.pop.coords
    #         last_move = 1
    #         fish_activity_time = time.time()
    #     else:
    #         pop_move__, last_move, fish_activity_time = pop_move(pop_y, new_fish, last_move, fish_activity_time)
    #         pop_y = pop_move__
    
    # Отрисовка окна
    screen.blit(background, (0, 0))  # отрисовка фона
    screen.blit(rod.image, rod.coords) # отрисовка удочки
    screen.blit(rod.pop.image, rod.pop.coords)  # отрисовка поплавка

    pg.display.update()
    clock.tick(FPS)

print('Конец')
pg.quit()