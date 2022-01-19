import requests
import pygame
import sys


BG = (20, 20, 20)
LIFECOLOR = (31, 97, 189)
LINECOLOR = (52, 53, 46)
LINE_WIDTH = 3
EDGE_WIDTH = 20
WIND_WIDTH = 440
WIND_HEIGHT = 440

CX = 40
CY = 40


class Game:
    screen = None

    def __init__(self, width, height, cx, cy, cells):
        self.width = width
        self.height = height
        self.cx_rate = int((width - 2 * EDGE_WIDTH) / cx)
        self.cy_rate = int((height - 2 * EDGE_WIDTH) / cy)
        self.screen = pygame.display.set_mode([width, height])
        self.cells = cells
        self.cx = cx
        self.cy = cy

    def show_life(self, new_cell):
        self.cells = new_cell

        for i in range(self.cx + 1):
            pygame.draw.line(self.screen, LINECOLOR, (EDGE_WIDTH, EDGE_WIDTH + i * self.cy_rate),
                             (EDGE_WIDTH + self.cx * self.cx_rate, EDGE_WIDTH + i * self.cy_rate),
                             LINE_WIDTH)
            pygame.draw.line(self.screen, LINECOLOR, (EDGE_WIDTH + i * self.cx_rate, EDGE_WIDTH),
                             (EDGE_WIDTH + i * self.cx_rate, EDGE_WIDTH + self.cy * self.cy_rate),
                             LINE_WIDTH)

        for cur_cell in self.cells:
            x = cur_cell['ix']
            y = cur_cell['iy']
            if cur_cell['is_live']:
                pygame.draw.rect(self.screen, LIFECOLOR,
                                 [EDGE_WIDTH + x * self.cx_rate + (LINE_WIDTH - 1),
                                  EDGE_WIDTH + y * self.cy_rate + (LINE_WIDTH - 1),
                                  self.cx_rate - LINE_WIDTH, self.cy_rate - LINE_WIDTH])


def main():
    pygame.init()
    pygame.display.set_caption("Conways Life")

    r = requests.get('http://127.0.0.1:16000/get_stage')
    game = Game(WIND_WIDTH, WIND_HEIGHT, CX, CY, r.json())

    clock = pygame.time.Clock()
    while True:
        game.screen.fill(BG)
        clock.tick(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        r = requests.get('http://127.0.0.1:16000/get_stage')
        game.show_life(r.json())
        pygame.display.flip()


if __name__ == '__main__':
    main()
