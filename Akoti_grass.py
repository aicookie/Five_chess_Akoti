import collections
import pygame as g
import sys
import time
from pygame import draw
from pygame.draw import aaline

# axis of coordinates
LINE_HORIZONTAL = 0             # ——    # horizontal axis # lateral
LINE_VERTICAL = 1               # |     # vertical axis # longitudinal
LINE_BISECTOR_QUADRANT_I = 2    # /     # Forward Slash
LINE_BISECTOR_QUADRANT_II = 3   # \     # Backward Slash
orientations = [(0, 0)] * 4
orientations[LINE_HORIZONTAL] = (0, 1)
orientations[LINE_VERTICAL] = (1, 0)
orientations[LINE_BISECTOR_QUADRANT_I] = (1, 1)
orientations[LINE_BISECTOR_QUADRANT_II] = (1, -1)

PLAYER_HUMAN = 1
PLAYER_AI = 2

TAB_X0, TAB_Y0 = 20, 20
CELL_W, CELL_H = 66, 64

xstep = 0
matrix = [[0] * 24 for _ in range(24)]


class Matrix:
    def __init__(self, node):
        self.node = node
        self.table = self._collect()

    def _collect(self):
        tab = [[0] * 19 for _ in range(19)]
        current = self.node
        n = current.depth() + 1
        while current.parent:
            y, x = current.coordinate
            n -= 1
            tab[y][x] = (n & 1) + 1
            current = current.parent
        return tab

    def crosslines(self, coordinate):
        def calc(orientation):
            return self.line(coordinate, orientation)
            y0, x0 = coordinate
            numb = 1
            who = self.table[y0][x0]
            y = y0 + orientation[0]
            x = x0 + orientation[1]
            while self.table[y][x] == who:
                numb += 1
                y += orientation[0]
                x += orientation[1]
            y = y0 - orientation[0]
            x = x0 - orientation[1]
            while self.table[y][x] == who:
                numb += 1
                y -= orientation[0]
                x -= orientation[1]
            return numb
        return map(calc, orientations)

    def line(self, coordinate, orientation):
        y0, x0 = coordinate  # if coordinate: y0, x0 = coordinate
        who = self.table[y0][x0]
        if not who:
            return []
        lis = [(y0, x0)]
        y = y0 + orientation[0]
        x = x0 + orientation[1]
        while self.table[y][x] == who:
            lis.append((y, x))
            y += orientation[0]
            x += orientation[1]
        y = y0 - orientation[0]
        x = x0 - orientation[1]
        while self.table[y][x] == who:
            lis.insert(0, (y, x))
            y -= orientation[0]
            x -= orientation[1]
        return lis

    def win(self, coordinate):
        # 2> 判断胜利
        lines = self.crosslines(coordinate)
        numbers = map(len, lines)
        if max(numbers) < 5:
            return False
        print(f'PLAYER {self.node.coordinate} step {self.node.depth()}: *WIN*')
        return True

    def empty(self, y, x):
        return not self.table[y][x]


class TreeNode:
    def __init__(self, parent):
        self.coordinate = (0, 0)
        self.parent = parent
        self.children = []

    def step(self, y, x):
        node = TreeNode(self)
        node.coordinate = (y, x)
        self.children.append(node)
        return node

    def depth(self):
        current = self
        n = 1
        while current.parent:
            current = current.parent
            n += 1
        return n


root = this = TreeNode(None)


def print_matrix(matrix):
    for xl in matrix:
        print(xl)
    print()


def draw_matrix(matrix):
    # 绘制背景图像
    screen.blit(bg, (0, 0))
    # 绘制所有棋子
    for (iy, row) in enumerate(matrix.table):
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
    # for a in sys.argv[1:]:
    #     x, y, z = eval(a)
    #     matrix[y][x] = z
    # print_matrix()
    draw_matrix(Matrix(root))

    while True:
        newstep = False
        evnet = None
        # 处理鼠标点击事件
        for event in g.event.get():
            if event.type == g.QUIT:
                g.quit()
            # time.sleep(0.5)
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            matrix = Matrix(this)
            x, y = pygame.mouse.get_pos()
            ix = int(x / CELL_W)
            iy = int(y / CELL_H)
            if not matrix.empty(iy, ix):
                continue

            node, matrix = player_step(iy, ix)
            if matrix.win(node.coordinate):  # player win
                continue

            node, matrix = ai_Step(matrix, (iy, ix))
            if matrix.win(node.coordinate):  # ai win
                continue

            # 2> 在屏幕绘制matrix
            draw_matrix(matrix)
            # print_matrix()


def player_step(iy, ix):
    global this
    node = this = this.step(iy, ix)
    matrix = Matrix(node)
    return node, matrix


def ai_Step(matrix, coordinate):
    global this
    node = this
    lines = list(matrix.crosslines(coordinate))
    ordered = sorted(range(len(lines)), key=lambda i: 99-len(lines[i]))
    for i in ordered:
        dy, dx = orientations[i]
        head, tail = lines[i][-1], lines[i][0]
        y, x = head
        y, x = y + dy, x + dx
        if matrix.empty(y, x):
            node = this = this.step(y, x)
            break
        y, x = tail
        y, x = y - dy, x - dx
        if matrix.empty(y, x):
            node = this = this.step(y, x)
            break
    matrix = Matrix(node)
    return node, matrix


def calculate(y, x):

    def count(name, y0, x0, orientation):
        spaces = {}
        count = 1
        who = matrix[y0][x0]
        y = y0 + orientation[0]
        x = x0 + orientation[1]
        while matrix[y][x] == who:
            count += 1
            y += orientation[0]
            x += orientation[1]
        spaces[(y, x)] = 1
        y = y0 - orientation[0]
        x = x0 - orientation[1]
        while matrix[y][x] == who:
            count += 1
            y -= orientation[0]
            x -= orientation[1]
        return count, name,

    orientations = (0, 1), (1, 0), (1, 1), (1, -1)
    names = LINE_HORIZONTAL, LINE_VERTICAL, LINE_BISECTOR_QUADRANT_I, LINE_BISECTOR_QUADRANT_II
    return [count(name, y, x, o) for o, name in zip(orientations, names)]


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


def win(iy, ix):
    # 2> 判断胜利
    cals = calculate(iy, ix)
    n, orientation = max(cals, key=lambda v: v[0])
    if n >= 5:
        print(f'PLAYER {matrix[iy][ix]}, step {xstep}: **WIN**')
        return orientation
    return None


def deep_search(iy, ix):
    pass


#   *: 当前空位置;

#   0: 其他空位置;

#   1: plyer(当前所计算的player的代号);

#   2: 3-plyer(对方的代号);

# */

# 1.活四 ：01111*

# 2.死四A ：21111*

# 3.死四B ：111*1

# 4.死四C ：11*11

# 5.活三（近三位置） ：111*0

# 6.活三（远三位置） ：1110*

# 7.死三            ：11*1

#     # if ai_calculate(iy, ix) >= 4:
#     #     print("The Game Result White+Resgin was added to the game information.")

#     # for i in range(15):
#     #     pass
#     return wid, hei


# 1> 初始化 骨 髓 随 便

def tree_search(iy, ix):
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
    return wid, hei
    pass


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
# ICAIC
