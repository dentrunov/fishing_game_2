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
bag = Bag()

#группируем спрайты
all_sprites = pg.sprite.Group()
# all_sprites.add(rod, pop)

# окно сумки
window = pg.Surface(( 800, 400))
window.fill((255, 255, 255))

def set_text(txt):
    '''функция подготовки текста'''
    screen.fill(COLOR_FILL)
    text_field = f1.render(txt, True, BLACK)
    screen.blit(text_field, (10, HEIGHT - 40))

def get_bag(fish=None):
    if fish is not None:
        bag.put_fish(fish)
    bag.opened = True    
    # window = pg.Surface(( 800, 400))
    # window.fill((255, 255, 255))
    text_field = f1.render(str(bag), True, BLACK)
    window.fill(COLOR_FILL)
    window.blit(text_field, (10, 100))
    # background.blit(window,)

def close_bag():
    bag.opened = False
    # window = pg.Surface((0, 0))
    # window.fill(())
    # background.blit(window, (-1000, -1000))

#подготовка текста
f1 = pg.font.SysFont('arial', 20)
set_text('Начало игры')


def fish_generate():
    ''' генерация клева рыбы '''
    # chance = [0] * 100 + [1]
    chance = [0] * 1000 + [1]
    if choice(chance):
        f = Fish(*choice(fish_names))
        rod.pop.transform((10, 20))
        # rod.pop.image = pg.transform.scale(rod.pop.image, (10, 20))  
        # rod.pop.coords = [rod.pop.coords[0], rod.pop.coords[1] - 20]
        tm = datetime.now()
        print(f'{f.name} {f.size} г. клюёт в {tm}')
        set_text(f'{f.name} {f.size} г. клюёт в {tm}')
        return f
    # return False

def pop_move(fish, fish_activity_time):
    '''анимация поклевки'''
    if rod.down:
        #генерируем паузу поклевки
        if time.time() - fish_activity_time > uniform(0.0, 2.0):
            # просчитываем прекращение клёва
            if not choice([1] * fish.heaviness * 10 + [0]):

                print('Перестала клевать')
                set_text('Перестала клевать')
                # return y, fish_activity_time
                return None
            y = rod.pop.last_move * 2
            rod.pop.last_move *= -1
            # if last_move == 1:
            #     last_move = 0
            #     y = 2
            # else:
            #     last_move = 1
            #     y = -2
            # if y < MAX_HEIGHT: y = MAX_HEIGHT
            # if y > HEIGHT - 5: y = HEIGHT - 5
            rod.pop.transform((rod.pop.size[0], rod.pop.size[1] + y))
            rod.pop.coords[1] -= y
            fish_activity_time = time.time()

    return fish_activity_time


#игровой цикл
game_over = True
while game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = False
            break
        if event.type == pg.KEYDOWN:
            # достаем и убираем удочку
            if event.key == pg.K_1:
                rod.get(*pg.mouse.get_pos())

            # открываем сумку (B)
            if event.key == pg.K_b:
                if not bag.opened:
                    get_bag()
                else:
                    close_bag()

            if event.key == pg.K_SPACE:
                #подсечка
                if rod.active and rod.down:
                    rod.get_fish()

        if event.type == pg.MOUSEBUTTONDOWN:
            # заброс удочки
            if event.button == 1:
                if rod.active and rod.down:
                    rod.put(*event.pos)

    # поклевка
    if all((rod.down, rod.active, rod.usable)):
        if rod.new_fish is None:
            rod.new_fish = fish_generate()
            fish_activity_time = time.time()
        else:
            fish_activity_time = pop_move(rod.new_fish, fish_activity_time)
    
    keys = pg.key.get_pressed()
    if keys[pg.K_f]:
        if rod.new_fish and rod.down:
            continue
        else:
            rod.roll()
            # get_bag(rod.new_fish)

    # Отрисовка окна
    screen.blit(background, (0, 0))  # отрисовка фона
    screen.blit(rod.image, rod.coords) # отрисовка удочки
    screen.blit(rod.pop.image, rod.pop.coords)  # отрисовка поплавка
    screen.blit(window, bag.coords) # отрисовка открытой сумки
    

    pg.display.update()
    clock.tick(FPS)

print('Конец')
pg.quit()