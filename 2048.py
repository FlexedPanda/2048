import random
import math
import copy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WINDOW_WIDTH  = 400
WINDOW_HEIGHT = 500
BOARD_SIZE = 4
BOARD_DIM = WINDOW_WIDTH

# Global Variables
COLORS = {
    'light': (249/255, 246/255, 242/255),
    'dark': (119/255, 110/255, 101/255),
    'screen': (200/255, 200/255, 200/255),
    'background': (187/255, 173/255, 160/255),
    'other': (0, 0, 0)
}

def get_color_for_block(number):
    if number == 0:
        return (0.8, 0.8, 0.8)

    max_value = 2048

    color_scale = math.log(number, 2) / math.log(max_value, 2)

    if color_scale < 0:
        color_scale = -color_scale

    red = color_scale

    green = (1 - color_scale)
    blue = (1 - color_scale)

    return (red, green, blue)


# Algs
def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

def convertZone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    else:
        return x, -y

def originalZone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    else:
        return x, -y

def midpointLineAlgo(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    x1, y1 = convertZone(x1, y1, zone)
    x2, y2 = convertZone(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1
    y = y1

    while x <= x2:
        org_x, org_y = originalZone(x, y, zone)
        glVertex2f(org_x, org_y)
        if d<0:
            d += incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1

def circlePoint(x, y, cx, cy, zone):
    for i in range(len(zone)):
        if zone[i]==1:
            glVertex2f(x + cx, y + cy)
        elif zone[i]==0:
            glVertex2f(y + cx, x + cy)
        elif zone[i]==7:
            glVertex2f(y + cx, -x + cy)
        elif zone[i]==6:
            glVertex2f(x + cx, -y + cy)
        elif zone[i]==5:
            glVertex2f(-x + cx, -y + cy)
        elif zone[i]==4:
            glVertex2f(-y + cx, -x + cy)
        elif zone[i]==3:
            glVertex2f(-y + cx, x + cy)
        elif zone[i]==2:
            glVertex2f(-x + cx, y + cy)

def midpointCircleAlgo(cx, cy, rad, zone):
    x, y = 0, rad
    d = 1 - rad

    circlePoint(x, y, cx, cy, zone)
    while x<y:
        if d<0:
            d += 2*x + 3
            x += 1
        else:
            d += 2*x - 2*y + 5
            x += 1
            y -= 1
        circlePoint(x, y, cx, cy, zone)

def drawLine(x1, y1, x2, y2, clr):
    glColor3fv(clr)
    glPointSize(3)
    glBegin(GL_POINTS)
    midpointLineAlgo(x1, y1, x2, y2)
    glEnd()

def drawCirc(x, y, rad, zone, clr):
    glColor3fv(clr)
    glPointSize(3)
    glBegin(GL_POINTS)
    midpointCircleAlgo(x, y, rad, zone)
    glEnd()


# Drawing Functions

def drawDigit(x1, y1, wdt, d, clr):
    x2, y2 = x1+wdt, y1+2*wdt
    w, h = x2-x1, y2-y1
    if d==0:
        drawCirc(x1+0.5*w, y1+0.75*h, 0.5*w, [0, 1, 2, 3], clr)
        drawCirc(x1+0.5*w, y1+0.25*h, 0.5*w, [7, 6, 5, 4], clr)
        drawLine(x1, y1+0.75*h, x1, y1+0.25*h, clr)
        drawLine(x2, y1+0.75*h, x2, y1+0.25*h, clr)

    elif d==1:
        drawLine(x1+0.5*w, y1, x1+0.5*w, y2, clr)
        drawLine(x1+0.5*w, y2, x1, y2-0.25*h, clr)

    elif d==2:
        drawCirc(x1+0.5*w, y1+0.75*h, 0.5*w, [0, 1, 2, 3], clr)
        drawLine(x2, y1+0.75*h, x1, y1, clr)
        drawLine(x1, y1, x2, y1, clr)

    elif d==3:
        drawCirc(x1+0.5*w, y1+0.75*h, 0.5*w, [0, 1, 2, 3, 7, 6], clr)
        drawCirc(x1+0.5*w, y1+0.25*h, 0.5*w, [0, 1, 7, 6, 4, 5], clr)

    elif d==4:
        drawLine(x1+0.75*w, y1, x1+0.75*w, y2, clr)
        drawLine(x1, y1+0.25*h, x2, y1+0.25*h, clr)
        drawLine(x1, y1+0.25*h, x1+0.75*w, y2, clr)

    elif d==5:
        drawCirc(x1+0.42*w, y1+0.29*h, 0.575*w, [0, 1, 2, 5, 6, 7], clr)
        drawLine(x1, y1+0.485*h, x1, y2, clr)
        drawLine(x1, y2, x2, y2, clr)

    elif d==6:
        drawCirc(x1+0.5*w, y1+0.25*h, 0.5*w, [0, 1, 2, 3, 4, 5, 6, 7], clr)
        drawLine(x1, y1+0.33*h, x2, y2, clr)

    elif d==7:
        drawLine(x1, y2, x2, y2, clr)
        drawLine(x1, y1, x2, y2, clr)

    elif d==8:
        drawCirc(x1+0.5*w, y1+0.75*h, 0.5*w, [0, 1, 2, 3, 4, 5, 6, 7], clr)
        drawCirc(x1+0.5*w, y1+0.25*h, 0.5*w, [0, 1, 2, 3, 4, 5, 6, 7], clr)

    elif d==9:
        drawCirc(x1+0.5*w, y1+0.75*h, 0.5*w, [0, 1, 2, 3, 4, 5, 6, 7], clr)
        drawLine(x2, y1+0.67*h, x1, y1, clr)

def drawNumber(x, y, w, h, num, clr):

    digits = [int(d) for d in str(num)]
    n = len(digits)
    maxDigitBoxWidth = 20
    width = min(maxDigitBoxWidth, w // n)
    initial_padding = 2

    start_x = x + ((w // 2) - (width * n) // 2)
    start_y = y + ((h - (width * 2)) // 2)

    for i in range(n):
        drawDigit(start_x + (i * width) + initial_padding, start_y, int(width * 0.8), digits[i], clr)

def getCellLocator(i, j):
    global BOARD_SIZE, BOARD_DIM
    padding = 20
    cell_dim = (BOARD_DIM - padding) // BOARD_SIZE
    return i*cell_dim + padding, j*cell_dim + padding, cell_dim - padding

def drawShade(x, y, w, h, clr):
    for i in range(x, x+w):
        drawLine(i, y, i, y + h, clr)

def drawBoard():
    global COLORS, BOARD_SIZE, BOARD_DIM
    padding = 20
    cell_dim = (BOARD_DIM - padding) // BOARD_SIZE
    for i in range(BOARD_DIM):
        drawLine(i, 0, i, BOARD_DIM, COLORS['background'])

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x, y, w = getCellLocator(i, j)
            drawShade(x, y, w, w, (0.8, 0.8, 0.8))

# Program Functions
# Drawing Class

class Box:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self):
        drawShade(self.x, self.y, self.w, self.w, self.color)


class Button(Box):
    def __init__(self, x, y, w, h, color, shape):
        super().__init__(x, y, w, h, color)
        self.shape = shape

    def draw(self):
        super().draw()
        #print(self.shape)
        for k, info in self.shape:
            if k == 0:
                x1, y1, x2, y2 = info
                drawLine(self.x + (self.w * x1), self.y + (self.h * y1), self.x + (self.w * x2), self.y + (self.h * y2), (0, 0, 0))
            else:
                xc, yc, r, zone = info
                drawCirc(self.x + (self.w * xc), self.y + (self.h * yc), (self.w * r), zone, (0, 0, 0))

    def isClicked(self, i, j):
        if i >= self.x and i <= self.x + self.w and j >= self.y and j <= self.y + self.h:
            return True
        else:
            return False


class Tile(Box):
    def __init__(self, x = 0, y = 0, w = 0, val = 0):
        self.value = val
        color = get_color_for_block(self.value)
        super().__init__(x, y, w, w, color)

    def update(self, x, y, w, val):
        self.x = x
        self.y = y
        self.w = w
        self.value = val
        self.color = get_color_for_block(self.value)

    def refresh_color(self):
        self.color = get_color_for_block(self.value)

    def draw(self):
        super().draw()
        if self.value != 0:
            drawNumber(self.x, self.y, self.w, self.w, self.value, (1, 1, 1))


class Game:
    def __init__(self, size):
        self.size = size
        self.animating = False
        self.animationDirection = None
        self.animations = []
        self.animationsDone = []
        self.values = None
        self.values_copy = None
        self.tiles = [[Tile() for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0
        self.point = 0
        self.best_score = 0
        self.reset()

    def drawTiles(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j].value != 0:
                    self.tiles[i][j].draw()

    def drawScore(self, color):
        drawNumber(WINDOW_WIDTH * 0.25, BOARD_DIM + 10, WINDOW_WIDTH * 0.25, WINDOW_HEIGHT - BOARD_DIM - 20, self.score, color)
        drawNumber(WINDOW_WIDTH * 0.50, BOARD_DIM + 10, WINDOW_WIDTH * 0.25, WINDOW_HEIGHT - BOARD_DIM - 20, self.best_score, (0.3, 0.8, 0.1))

    def updateTiles(self):
        for i in range(self.size):
            for j in range(self.size):
                x, y, w = getCellLocator(i, j)
                val = self.values[i][j]
                self.tiles[i][j].update(x, y, w, val)

    def full(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.values[i][j] == 0:
                    return False
        return True

    def over(self):
        if not self.full():
            return False
        for i in range(self.size):
            for j in range(self.size):
                if i - 1 >= 0:
                    if self.values[i][j] == self.values[i - 1][j]:
                        return False
                if i + 1 < self.size:
                    if self.values[i][j] == self.values[i + 1][j]:
                        return False
                if j - 1 >= 0:
                    if self.values[i][j] == self.values[i][j - 1]:
                        return False
                if j + 1 < self.size:
                    if self.values[i][j] == self.values[i][j + 1]:
                        return False
        return True

    def spawnNewTile(self):
        if not self.over():
            i, j = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while self.values[i][j] != 0:
                i, j = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.values[i][j] = 2
        self.updateTiles()

    def step(self, to):
        global game_over
        self.values_copy = copy.deepcopy(self.values)
        self.point = 0
        if to == "UP":
            self.animationDirection = "UP"
            for i in range(self.size):
                merged = [False for _ in range(self.size)]
                for j in range(self.size - 2, -1, -1):
                    have = self.values_copy[i][j]
                    if have == 0:
                        continue
                    k = 0
                    got = 0
                    for k in range(j + 1, self.size):
                        got = self.values_copy[i][k]
                        if got != 0:
                            break

                    if got == 0:
                        self.values_copy[i][k] = have
                        self.values_copy[i][j] = 0
                        self.animations.append(((i, j), (i, k)))
                    else:
                        if got != have or merged[k]:
                            if j != k - 1:
                                self.values_copy[i][k - 1] = have
                                self.values_copy[i][j] = 0
                                self.animations.append(((i, j), (i, k - 1)))
                        else:
                            if not merged[k]:
                                merged[k] = True
                                self.values_copy[i][k] = 2 * have
                                self.values_copy[i][j] = 0
                                self.point += self.values_copy[i][k]
                                self.animations.append(((i, j), (i, k)))


        elif to == "DOWN":
            self.animationDirection = "DOWN"
            for i in range(self.size):
                merged = [False for _ in range(self.size)]
                for j in range(1, self.size):
                    have = self.values_copy[i][j]
                    if have == 0:
                        continue
                    k = 0
                    got = 0
                    for k in range(j - 1, -1, -1):
                        got = self.values_copy[i][k]
                        if got != 0:
                            break

                    if got == 0:
                        self.values_copy[i][k] = have
                        self.values_copy[i][j] = 0
                        self.animations.append(((i, j), (i, k)))
                    else:
                        if got != have or merged[k]:
                            if j != k + 1:
                                self.values_copy[i][k + 1] = have
                                self.values_copy[i][j] = 0
                                self.animations.append(((i, j), (i, k + 1)))
                        else:
                            if not merged[k]:
                                merged[k] = True
                                self.values_copy[i][k] = 2 * have
                                self.values_copy[i][j] = 0
                                self.point += self.values_copy[i][k]
                                self.animations.append(((i, j), (i, k)))
        elif to == "RIGHT":
            self.animationDirection = "RIGHT"
            for i in range(self.size):
                merged = [False for _ in range(self.size)]
                for j in range(self.size - 2, -1, -1):
                    have = self.values_copy[j][i]
                    if have == 0:
                        continue
                    k = 0
                    got = 0
                    for k in range(j + 1, self.size):
                        got = self.values_copy[k][i]
                        if got != 0:
                            break

                    if got == 0:
                        self.values_copy[k][i] = have
                        self.values_copy[j][i] = 0
                        self.animations.append(((j, i), (k, i)))
                    else:
                        if got != have or merged[k]:
                            if j != k -1:
                                self.values_copy[k - 1][i] = have
                                self.values_copy[j][i] = 0
                                self.animations.append(((j, i), (k - 1, i)))
                        else:
                            if not merged[k]:
                                merged[k] = True
                                self.values_copy[k][i] = 2 * have
                                self.values_copy[j][i] = 0
                                self.point += self.values_copy[k][i]
                                self.animations.append(((j, i), (k, i)))
        elif to == "LEFT":
            self.animationDirection = "LEFT"
            for i in range(self.size):
                merged = [False for _ in range(self.size)]
                for j in range(1, self.size):
                    have = self.values_copy[j][i]
                    if have == 0:
                        continue
                    k = 0
                    got = 0
                    for k in range(j - 1, -1, -1):
                        got = self.values_copy[k][i]
                        if got != 0:
                            break

                    if got == 0:
                        self.values_copy[k][i] = have
                        self.values_copy[j][i] = 0
                        self.animations.append(((j, i), (k, i)))
                    else:
                        if got != have or merged[k]:
                            if j != k + 1:
                                self.values_copy[k + 1][i] = have
                                self.values_copy[j][i] = 0
                                self.animations.append(((j, i), (k + 1, i)))
                        else:
                            if not merged[k]:
                                merged[k] = True
                                self.values_copy[k][i] = 2 * have
                                self.values_copy[j][i] = 0
                                self.point += self.values_copy[k][i]
                                self.animations.append(((j, i), (k, i)))

        # for j in range(len(self.values) - 1, -1, -1):
        #     for i in range(len(self.values)):
        #         print(self.values[i][j], end = ' ')
        #     print()
        # print()
        #print(self.animations)

        if len(self.animations) > 0:
            self.animating = True
            self.animationsDone = [False] * len(self.animations)

        self.updateTiles()
        if self.over():
            game_over = True

    def animationCompleted(self):
        for check in self.animationsDone:
            if not check:
                return False
        return True

    def reset(self):
        global game_over
        self.values = [[0 for _ in range(self.size)] for _ in range(self.size)]

        i, j = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        ii, jj = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        while((ii, jj) == (i, j)):
            ii, jj = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        
        self.values[i][j] = 2
        self.values[ii][jj] = 2

        if self.score > self.best_score:
            self.best_score = self.score

        self.score = 0
        game_over = False
        self.updateTiles()



game = Game(BOARD_SIZE)
max_score = 0
game_over = False
last_frame_time = 0

RESET_BUTTON_SHAPE = [(1, (0.5, 0.5, 0.3, (0, 1, 2, 3, 4, 5, 7))), (0, (0.5, 0.2, 0.5 - 0.125, 0.2 + 0.125)), (0, (0.5, 0.2, 0.5 - 0.125, 0.2 - 0.1))]
resetButton = Button(10, BOARD_DIM + 10, WINDOW_HEIGHT - BOARD_DIM - 20, WINDOW_HEIGHT - BOARD_DIM - 20, (0.9, 1, 0.9), RESET_BUTTON_SHAPE)

EXIT_BUTTON_SHAPE = [(0, (0.2, 0.2, 0.8, 0.8)), (0, (0.8, 0.2, 0.2, 0.8))]
exitButton = Button(int(WINDOW_WIDTH * 0.75) + 10, BOARD_DIM + 10, WINDOW_HEIGHT - BOARD_DIM - 20, WINDOW_HEIGHT - BOARD_DIM - 20, (1, 0.9, 0.9), EXIT_BUTTON_SHAPE)

# GL Functions
def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def show_screen():
    global COLORS, game_over
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(COLORS['screen'][0], COLORS['screen'][1], COLORS['screen'][2], 1.0)

    drawBoard()
    game.drawTiles()
    resetButton.draw()
    exitButton.draw()

    if game_over:
        color = (1, 0, 0)
    else:
        color = (0, 0, 0)
    game.drawScore(color)

    glutSwapBuffers()

def animation():
    global game, last_frame_time

    speed = 200

    # Getting framerate independency
    current_time = glutGet(GLUT_ELAPSED_TIME)
    time_difference = current_time - last_frame_time
    last_frame_time = current_time
    delta_time = time_difference / 1000.0

    if game.animating:
        for ii, animation_task in enumerate(game.animations):
            if not game.animationsDone[ii]:
                done = False
                (i, j), (target_i, target_j) = animation_task
                #assert(not (game.values[target_i][target_j] != 0 and game.values[target_i][target_j] != game.values[i][j]))

                tx, ty, _ = getCellLocator(target_i, target_j)
                step = max(abs(target_i - i), abs(target_j - j))
                if game.animationDirection == "UP":
                    game.tiles[i][j].y += int(step * delta_time * speed)
                    if game.tiles[i][j].y >= ty:
                        done = True
                elif game.animationDirection == "DOWN":
                    game.tiles[i][j].y -= int(step * delta_time * speed)
                    if game.tiles[i][j].y <= ty:
                        done = True
                elif game.animationDirection == "RIGHT":
                    game.tiles[i][j].x += int(step * delta_time * speed)
                    if game.tiles[i][j].x >= tx:
                        done = True
                else:
                    game.tiles[i][j].x -= int(step * delta_time * speed)
                    if game.tiles[i][j].x <= tx:
                        done = True

                game.tiles[i][j].refresh_color()

                if done:
                    # game.values[target_i][target_j] = game.values_copy[i][j]
                    # game.values[i][j] = 0
                    game.animationsDone[ii] = True

        if game.animationCompleted():
            game.values = copy.deepcopy(game.values_copy)
            if not game.full():
                game.spawnNewTile()
            game.animations = []
            game.animating = False
            game.animationsDone = []
            game.score += game.point
            game.updateTiles()

    if glutGetWindow():
        glutPostRedisplay()

def keyboard_ordinary_keys(key, _, __):

    if glutGetWindow():
        glutPostRedisplay()

def keyboard_special_keys(key, _, __):
    global game, game_over
    if not game_over and not game.animating:
        if key == GLUT_KEY_UP:
            game.step("UP")
        elif key == GLUT_KEY_DOWN:
            game.step("DOWN")
        elif key == GLUT_KEY_LEFT:
            game.step("LEFT")
        elif key == GLUT_KEY_RIGHT:
            game.step("RIGHT")

    if glutGetWindow():
        glutPostRedisplay()

def mouse_click(button, state, x, y):
    global wind

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mx, my = x, WINDOW_HEIGHT - y

            if resetButton.isClicked(mx ,my):
                game.reset()

            if exitButton.isClicked(mx, my):
                glutDestroyWindow(wind)

    if glutGetWindow():
        glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"2048")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)

glutKeyboardFunc(keyboard_ordinary_keys)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_click)

# glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()
