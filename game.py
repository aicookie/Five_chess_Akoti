import pygame as g
import time

from pygame.draw import aaline
pygame = g
g.init()
pygame.display.init()
screen = g.display.set_mode((1000, 1000))
bg = pygame.image.load("fcb7bf11701da82fa08c033a431872ac.jpeg")
screen.blit(bg, (0, 0))
who = 1

TAB_X0, TAB_Y0 = 20, 20
CELL_W, CELL_H = 66, 64

matrix = [[0] * 24 for _ in range(24)]

for xl in matrix:
    print(xl)

wc = pygame.image.load("whitechess.png")
bc = pygame.image.load("blackchess.png")

max([1, 7, 3, 5, 9])


def calculate(y, x):
    def count(y0, x0, u):
        count = 1
        who = matrix[y0][x0]
        y = y0 + u[0]
        x = x0 + u[1]
        while matrix[y][x] == who:
            count += 1
            y += u[0]
            x += u[1]
        y = y0 - u[0]
        x = x0 - u[1]
        while matrix[y][x] == who:
            count += 1
            y -= u[0]
            x -= u[1]
        return count

    return max([count(y, x, (0, 1)), count(y, x, (1, 0)), count(y, x, (1, 1)), count(y, x, (1, -1))])


while True:

    for event in g.event.get():
        if event.type == g.QUIT:
            g.quit()

    # 绘制背景图像
    # 1> 加载图像
    wce = pygame.transform.scale(wc, (50, 50))
    bce = pygame.transform.scale(bc, (50, 50))
    x, y = pygame.mouse.get_pos()
    # x -= wce.get_width() / 2
    # y -= wce.get_height() / 2

    # for y in range(0, 900, TAB_H):
    #    for x in range(0, 900, TAB_W):
    #        screen.blit(wce, (x + 20, y + 20))

    if event.type == pygame.MOUSEBUTTONDOWN:
        ix = int(x / CELL_W)
        iy = int(y / CELL_H)
        px = ix * CELL_W + TAB_X0
        py = iy * CELL_H + TAB_Y0
        print(f"x: {x} {ix} {px} \ty: {y} {iy} {py} \t: {matrix[iy][ix]}")
        if not matrix[iy][ix]:
            matrix[iy][ix] = who
            if who == 1:
                screen.blit(bce, (px, py))
                who = 2
            elif who == 2:
                screen.blit(wce, (px, py))
                who = 1
            for xl in matrix:
                print(xl)
            if calculate(iy, ix) >= 5:
                print(f'who={matrix[iy][ix]} WIN!!!!')
        time.sleep(0.2)

    # 2> 绘制在屏幕

    # screen.blit(bce, (90, 90))
    run = True
    # 3> 更新显示
    pygame.display.update()
