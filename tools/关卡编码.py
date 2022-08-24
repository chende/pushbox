def encode_level(grid):
    """
    将关卡信息编码为一个字符串, 数字表示砖块信息，字母表示次数
    """
    a2z = 'abcdefghijklmnopqrstuvwxyz'
    encoded = ''
    height = len(grid)
    width = len(grid[0])
    encoded = write_value(encoded, width, '_')
    encoded = write_value(encoded, height, '_')
    length = 0
    tile = grid[0][0]
    for i in range(height):
        for j in range(width):
            if length < 26 and grid[i][j] == tile:
                length += 1
            else:
                encoded = write_value(encoded, tile, a2z[length - 1])
                length = 1
                tile = grid[i][j]
    encoded = write_value(encoded, tile, a2z[length - 1])
    return encoded


def write_value(level_str, value, delimiter):
    level_str += str(value)
    level_str += delimiter
    return level_str


def decode_level(encoded):
    """
    将用 encode_level2 编码关卡信息得到的字符串，解码成二维列表
    """
    a2z = 'abcdefghijklmnopqrstuvwxyz'
    read_index = 0
    width, read_index = read_value(encoded, read_index)
    height, read_index = read_value(encoded, read_index)
    # 创建一个值都为 0 的二维列表
    grid = [[0 for i in range(width)] for j in range(height)]
    tile_index = 0
    while read_index < len(encoded):
        tile, read_index = read_value(encoded, read_index)
        times = a2z.find(encoded[read_index - 1]) + 1
        # 将取得的某个地图信息按次数放到对应二维列表对应位置
        for i in range(times):
            tile_grid_x = tile_index % width
            tile_grid_y = tile_index // width
            grid[tile_grid_y][tile_grid_x] = tile
            tile_index += 1
    return grid


def read_value(level_str, index):
    value_str = ''
    while '0' <= level_str[index] <= '9':
        value_str += level_str[index]
        index += 1
    index += 1
    value = int(value_str)
    return value, index


# 可以修改 grid，输出结果，通过对比猜测编码规则
grid1 = [[1, 1, 1],
         [1, 1, 1]]

grid2 = [[1, 1, 1],
         [1, 1, 1],
         [2, 2, 2]]

grid3 = [
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 4, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 4, 6, 1, 0, 1, 0, 0, 0, 3, 1],
    [1, 1, 1, 4, 1, 1, 1, 0, 0, 0, 3, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
]

grid7 = [
    [0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 3, 2, 2, 2, 1],
    [1, 2, 2, 4, 4, 4, 2, 2, 1],
    [1, 3, 1, 1, 3, 1, 1, 3, 1],
    [1, 2, 2, 2, 4, 2, 2, 2, 1],
    [1, 2, 2, 4, 3, 1, 2, 1, 1],
    [1, 1, 1, 1, 2, 2, 2, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 0]
]

grid8 = [
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 3, 2, 3, 3, 1, 0],
    [0, 1, 3, 2, 4, 3, 1, 0],
    [1, 1, 1, 2, 2, 4, 1, 1],
    [1, 2, 4, 2, 2, 4, 2, 1],
    [1, 2, 1, 4, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

grid9 = [
    [0, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 2, 2, 2, 1],
    [1, 1, 1, 4, 2, 2, 1],
    [1, 2, 2, 2, 4, 1, 1],
    [1, 2, 3, 2, 3, 1, 0],
    [1, 1, 2, 4, 3, 1, 0],
    [0, 1, 2, 2, 2, 1, 0],
    [0, 1, 1, 1, 1, 1, 0]
]

# step1、运行以下代码，查看输出结果，分析 encode_level() 和 decode_level() 函数的作用
en_grid1 = encode_level(grid1)
print("grid1 编码结果是：", en_grid1)
print("en_grid1 解码结果是：", decode_level(en_grid1))

en_grid2 = encode_level(grid2)
print("grid2 编码结果是：", en_grid2)
print("en_grid2 解码结果是：", decode_level(en_grid2))

# step2、尝试自己创建关卡信息，验证自己的猜想
en_grid3 = encode_level(grid3)
print("grid3 编码结果是：", en_grid3)
print("en_grid3 解码结果是：", decode_level(en_grid3))

en_grid7 = encode_level(grid7)
print("grid7 编码结果是：", en_grid7)
print("en_grid7 解码结果是：", decode_level(en_grid7))

en_grid8 = encode_level(grid8)
print("grid8 编码结果是：", en_grid8)
print("en_grid8 解码结果是：", decode_level(en_grid8))

en_grid9 = encode_level(grid9)
print("grid9 编码结果是：", en_grid9)
print("en_grid9 解码结果是：", decode_level(en_grid9))

en_grid4 = '6_6_0b1c0c1a3a1e2b1b3a4b2a1c2c1a0a1e'
en_grid5 = '7_7_1h3a1a2c1b3a2c3a1b2c4a2a1e4b1a0c1a2b1a0c1d'
en_grid6 = '7_8_0b1e0b1a2c1d4a2b1b2c4a1c2a3a2a3a1a0a1b2a4a3a1a0b1b2b1a0c1d0a'

print("en_grid4 解码结果是：", decode_level(en_grid4))
print("en_grid5 解码结果是：", decode_level(en_grid5))
print("en_grid6 解码结果是：", decode_level(en_grid6))
