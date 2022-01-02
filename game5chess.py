import pygame as g
import sys
import time
from pygame import draw
from pygame.draw import aaline

# axis of coordinates
LINE_HORIZONTAL = 1             # ——    # horizontal axis # lateral
LINE_VERTICAL = 2               # |     # vertical axis # longitudinal
LINE_BISECTOR_QUADRANT_I = 3    # /     # Forward Slash
LINE_BISECTOR_QUADRANT_II = 4   # \     # Backward Slash

PLAYER_HUMAN = 1
PLAYER_AI = 2

TAB_X0, TAB_Y0 = 20, 20
CELL_W, CELL_H = 66, 64

xstep = 0
matrix = [[0] * 24 for _ in range(24)]


def calculate(y, x):
    def count(y0, x0, orientation):
        count = 1
        step = matrix[y0][x0]
        y = y0 + orientation[0]
        x = x0 + orientation[1]
        while matrix[y][x] == step:
            count += 1
            y += orientation[0]
            x += orientation[1]
        y = y0 - orientation[0]
        x = x0 - orientation[1]
        while matrix[y][x] == step:
            count += 1
            y -= orientation[0]
            x -= orientation[1]
        return count

    orientations = (0, 1), (1, 0), (1, 1), (1, -1)
    names = LINE_HORIZONTAL, LINE_VERTICAL, LINE_BISECTOR_QUADRANT_I, LINE_BISECTOR_QUADRANT_II
    return [(count(y, x, o), name) for o, name in zip(orientations, names)]


def ai_calculate(y, x):
    def count(y0, x0, u):
        count = 1
        step = matrix[y0][x0]
        y = y0 + u[0]
        x = x0 + u[1]
        while matrix[y][x] == step:
            count += 1
            y += u[0]
            x += u[1]
        y = y0 - u[0]
        x = x0 - u[1]
        while matrix[y][x] == step:
            count += 1
            y -= u[0]
            x -= u[1]
        return count
    orientations = (0, 1), (1, 0), (1, 1), (1, -1)
    return max(count(y, x, o) for o in orientations)


def print_matrix():
    for xl in matrix:
        print(xl)
    print()


def draw_matrix():
    # 绘制背景图像
    screen.blit(bg, (0, 0))
    # 绘制所有棋子
    for (iy, row) in enumerate(matrix):
        for (ix, who) in enumerate(row):
            if not who:
                continue
            px = ix * CELL_W + TAB_X0
            py = iy * CELL_H + TAB_Y0
            if who == 1:
                screen.blit(bce, (px, py))
            else:
                screen.blit(wce, (px, py))
    # 3> 更新显示
    pygame.display.update()


def main():
    for a in sys.argv[1:]:
        x, y, z = eval(a)
        matrix[y][x] = z
    print_matrix()
    draw_matrix()

    while True:
        newstep = False
        evnet = None
        # 处理鼠标点击事件
        for event in g.event.get():
            if event.type == g.QUIT:
                g.quit()
            # time.sleep(0.5)
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            ix = int(x / CELL_W)
            iy = int(y / CELL_H)
            if matrix[iy][ix]:
                continue

            player_step(iy, ix)
            if win(iy, ix):
                continue

            iy, ix = ai_Step(iy, ix)
            if win(iy, ix):
                continue

            # 2> 在屏幕绘制matrix
            draw_matrix()
            # print_matrix()


def win(iy, ix):
    # 2> 判断胜利
    cals = calculate(iy, ix)
    n, orientation = max(cals, key=lambda v: v[0])
    if n >= 5:
        print(f'PLAYER {matrix[iy][ix]}, step {xstep}: **WIN**')
        return orientation
    return None


def player_step(iy, ix):
    global xstep
    matrix[iy][ix] = PLAYER_HUMAN  # (xstep & 1)+1
    xstep += 1


def ai_step(iy, ix):
    global xstep
    xstep += 1
    # if who == 2:
    #     if iy != 7 and ix != 7:
    #         matrix[7][7] = who
    #     else:
    #         deep_search(iy, ix)
    #     pass
    if matrix[iy+1][ix+1] == 1 or matrix[iy+1][ix+1] == 2:
        if matrix[iy+1][ix-1] == 1 or matrix[iy+1][ix-1] == 2:
            matrix[iy+1][ix] = PLAYER_AI
            pass
        else:
            matrix[iy+1][ix-1] = PLAYER_AI

    else:
        matrix[iy+1][ix+1] = PLAYER_AI
        pass
    # else:
    #     pass


def ai_Step(iy, ix):
    global xstep
    if not matrix[7][7]:
        matrix[7][7] = PLAYER_AI
        xstep += 1
        return 7, 7
    else:
        y, x = deep_search(iy, ix)
        matrix[y][x] = PLAYER_AI
        xstep += 1
        return y, x


def deep_search(iy, ix):
    wid = iy
    hei = ix
    cals = calculate(iy, ix)
    n, orientation = max(cals, key=lambda v: v[0])
    print(f'deep-search {iy},{ix}: {n} {orientation}')

    if orientation == LINE_HORIZONTAL:  # ——    # horizontal axis # lateral
        hei += 1
        pass
    elif orientation == LINE_VERTICAL:  # |     # vertical axis # longitudinal
        wid += 1
        pass
    elif orientation == LINE_BISECTOR_QUADRANT_I:  # /     # Forward Slash
        wid += 1
        hei += 1
        pass
    elif orientation == LINE_BISECTOR_QUADRANT_II:  # \     # Backward Slash
        wid -= 1
        hei += 1
        pass

    # if ai_calculate(iy, ix) >= 4:
    #     print("The Game Result White+Resgin was added to the game information.")

    # for i in range(15):
    #     pass
    return wid, hei


# 1> 初始化 骨 髓 随 便
pygame = g
g.init()
pygame.display.init()
screen = g.display.set_mode((1000, 1000))

# 1> 加载图像
bg = pygame.image.load("board.jpeg")
wc = pygame.image.load("whitechess.png")
bc = pygame.image.load("blackchess.png")
wce = pygame.transform.scale(wc, (50, 50))
bce = pygame.transform.scale(bc, (50, 50))

# for y in range(0, 900, TAB_H):
#    for x in range(0, 900, TAB_W):
#        screen.blit(wce, (x + 20, y + 20))
main()
