import turtle
from tools import media_tool
from pydub import AudioSegment
from pydub.playback import play


# 加载关卡
def load_level(store_list, level_num):
    global GRID, WIDTH, HEIGHT, player_grid_x, player_grid_y
    a2z = 'abcdefghijklmnopqrstuvwxyz'
    encoded = store_list[level_num - 1]
    read_index = 0
    player_grid_x, read_index = read_value(encoded, read_index)
    player_grid_y, read_index = read_value(encoded, read_index)
    WIDTH, read_index = read_value(encoded, read_index)
    HEIGHT, read_index = read_value(encoded, read_index)
    GRID = [[None for i in range(WIDTH)] for j in range(HEIGHT)]
    tile_index = 0
    while read_index < len(encoded):
        tile, read_index = read_value(encoded, read_index)
        times = a2z.find(encoded[read_index - 1]) + 1
        for i in range(times):
            tile_grid_x = tile_index % WIDTH
            tile_grid_y = tile_index // WIDTH
            GRID[tile_grid_y][tile_grid_x] = tile
            tile_index += 1
    print(GRID)


def read_value(level_string, index):
    value_str = ''
    while '0' <= level_string[index] <= '9':
        value_str += level_string[index]
        index += 1
    index += 1
    value = int(value_str)
    return value, index


def move_up():
    global movement_grid_y
    movement_grid_y = -1


def move_down():
    global movement_grid_y
    movement_grid_y = 1


def move_left():
    global movement_grid_x
    movement_grid_x = -1


def move_right():
    global movement_grid_x
    movement_grid_x = 1


def next_level(x, y):
    global level_num, level_gap
    level_num += 1
    win_or_lose.hideturtle()
    level_gap = False


def reload_level():
    global level_num, level_store
    load_level(level_store, level_num)


def is_wall(grid_x, grid_y, grid):
    return grid[grid_y][grid_x] == 1


def is_box(grid_x, grid_y, grid):
    return grid[grid_y][grid_x] == 4 or grid[grid_y][grid_x] == 5


# 关卡存放表，每一项用字符串表示关卡信息
level_store = ['4_3_6_6_0b1c0c1a3a1e2b1b3a4b2a1c2c1a0a1e',
               '4_5_7_7_1h3a1a2c1b3a2c3a1b2c4a2a1e4b1a0c1a2b1a0c1d',
               '5_2_7_8_0b1e0b1a2c1d4a2b1b2c4a1c2a3a2a3a1a0a1b2a4a3a1a0b1a2c1a0b1e0a',
               '7_1_9_8_0c1j3a2c1b2b4c2b1b3a1b3a1b3a1b2c4a2c1b2b4a3a1a2a1f2c1a0d1e0a',
               '4_6_8_8_0a1f0b1a3a2a3b1a0b1a3a2a4a3a1a0a1c2b4a1c2a4a2b4a2a1b2a1a4a1b2a1b2f1i'
               ]
# 关卡初始化
SIZE = 70
GRID = []
WIDTH = 0
HEIGHT = 0
player_grid_x = 0
player_grid_y = 0
level_num = 1
level_num_pre = 1
level_gap = False
load_level(level_store, level_num)
# 左上角砖块中心坐标
origin_x = 0 - SIZE * (WIDTH / 2 - 0.5)
origin_y = 0 + SIZE * (HEIGHT / 2 - 0.5)

# 添加素材
skindir = 'skin1/'
tile_shapes = [skindir + '空.gif', skindir + '墙壁.gif', skindir + '通道.gif', skindir + '目标.gif',
               skindir + '箱子.gif', skindir + '目标箱子.gif']
for i in tile_shapes:
    turtle.addshape(i)
turtle.addshape(skindir + '编程猫.gif')
turtle.addshape(skindir + '成功.gif')
turtle.addshape(skindir + '通关.gif')
# 初始化砖块和玩家画笔
tile = turtle.Pen()
tile.penup()
player = turtle.Pen()
player.shape(skindir + '编程猫.gif')
player.penup()

movement_grid_x = 0
movement_grid_y = 0

success_sound = AudioSegment.from_file("resources/success.wav", format="wav")
# play(success_sound)
success_level = False

# 监听
turtle.onkeyrelease(move_up, 'Up')
turtle.onkeyrelease(move_down, 'Down')
turtle.onkeyrelease(move_left, 'Left')
turtle.onkeyrelease(move_right, 'Right')
turtle.onkeyrelease(reload_level, 'r')
turtle.listen()

turtle.tracer(False)
while True:
    # 读取下一关卡
    if level_num != level_num_pre:
        load_level(level_store, level_num)
        # 左上角砖块中心坐标
        origin_x = 0 - SIZE * (WIDTH / 2 - 0.5)
        origin_y = 0 + SIZE * (HEIGHT / 2 - 0.5)
        level_num_pre = level_num

    if not level_gap:
        # 清空地图
        tile.clear()
        player.clear()
        # 计算移动量
        player_grid_x += movement_grid_x
        player_grid_y += movement_grid_y
        if is_wall(player_grid_x, player_grid_y, GRID):
            player_grid_x -= movement_grid_x
            player_grid_y -= movement_grid_y
        elif is_box(player_grid_x, player_grid_y, GRID):
            box_next_x = player_grid_x + movement_grid_x
            box_next_y = player_grid_y + movement_grid_y
            if is_box(box_next_x, box_next_y, GRID) or is_wall(box_next_x, box_next_y, GRID):
                player_grid_x -= movement_grid_x
                player_grid_y -= movement_grid_y
            else:
                GRID[box_next_y][box_next_x] += 2
                GRID[player_grid_y][player_grid_x] -= 2

        movement_grid_x = 0
        movement_grid_y = 0

        # 刷新地图
        for i in range(len(GRID)):
            for j in range(len(GRID[i])):
                tile.shape(tile_shapes[GRID[i][j]])
                tile.goto(origin_x + j * SIZE, origin_y - i * SIZE)
                tile.stamp()

        # 刷新player
        player.goto(origin_x + player_grid_x * SIZE, origin_y - player_grid_y * SIZE)
        player.stamp()

        # 胜负判断
        win_flag = True
        for i in GRID:
            if 3 in i:
                win_flag = False
                break

    if win_flag and not level_gap:
        win_or_lose = turtle.Pen()
        level_gap = True
        if level_num < len(level_store):
            win_or_lose.shape(skindir + '成功.gif')
            success_level = True
            win_or_lose.onclick(next_level)
        else:
            win_or_lose.shape(skindir + '通关.gif')

    turtle.update()

    # Play sound
    if (success_level):
        play(success_sound)
        success_level = False

turtle.done()
