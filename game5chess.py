import pygame as g
import sys
import time
from pygame import draw
from pygame.draw import aaline

TAB_X0, TAB_Y0 = 20, 20
CELL_W, CELL_H = 66, 64

xstep = 0
matrix = [[0] * 24 for _ in range(24)]


def calculate(y, x):
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
    return max([count(y, x, (0, 1)), count(y, x, (1, 0)), count(y, x, (1, 1)), count(y, x, (1, -1))])


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
    return ([count(y, x, (0, 1)), count(y, x, (1, 0)), count(y, x, (1, 1)), count(y, x, (1, -1))])


def print_matrix():
    for xl in matrix:
        print(xl)


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
            global xstep
            x, y = pygame.mouse.get_pos()
            ix = int(x / CELL_W)
            iy = int(y / CELL_H)
            if matrix[iy][ix]:
                continue
            matrix[iy][ix] = (xstep & 1)+1
            xstep += 1
            ai_step(2, iy, ix)
            xstep += 1
            # print_matrix()
            print()
            # 2> 判断胜利
            if calculate(iy, ix) >= 5:
                print(f'xstep {xstep} {matrix[iy][ix]} **WIN**')
            # 2> 在屏幕绘制matrix
            draw_matrix()
            #print( f"x: {x} {ix} {px} \ty: {y} {iy} {py} \t: {matrix[iy][ix]}")


def ai_step(who, iy, ix):
    # if who == 2:
    #     if iy != 7 and ix != 7:
    #         matrix[7][7] = who
    #     else:
    #         deep_search(iy, ix)
    #     pass
    if matrix[iy+1][ix+1] == 1 or matrix[iy+1][ix+1] == 2:
        if matrix[iy+1][ix-1] == 1 or matrix[iy+1][ix-1] == 2:
            matrix[iy+1][ix] = who
            pass
        else:
            matrix[iy+1][ix-1] = who

    else:
        matrix[iy+1][ix+1] = who
        pass
    # else:
    #     pass


def deep_search(iy, ix):
    # if calculate(iy, ix) >= 4:
    #     print("The Game Result White+Resgin was added to the game information.")
    for i in range(15):
        pass

    pass


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
