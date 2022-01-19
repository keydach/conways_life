import random
from fastapi import APIRouter
from typing import List
from models.cell import OutCell


class Cell:

    def __init__(self, grid, ix, iy, is_live):
        self.grid = grid
        self.ix = ix
        self.iy = iy
        self.is_live = is_live
        self.neighbour_count = 0

    def calc_neighbour_count(self):
        count = 0
        neighbour_coord = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

        for coord in neighbour_coord:
            cur_x = self.ix + coord[0]
            if cur_x < 0:
                cur_x = self.grid.cx - 1
            elif cur_x == self.grid.cx:
                cur_x = 0

            cur_y = self.iy + coord[1]
            if cur_y < 0:
                cur_y = self.grid.cy - 1
            elif cur_y == self.grid.cy:
                cur_y = 0

            count += int(self.grid.cells[cur_x][cur_y].is_live)

        self.neighbour_count = count
        return count

    def rule(self):
        if self.neighbour_count > 3 or self.neighbour_count < 2:
            self.is_live = False
        elif self.neighbour_count == 3:
            self.is_live = True


class Grid:

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.cells = []

        for i in range(self.cx):
            cell_list = []
            for j in range(self.cy):
                cell = Cell(self, i, j, random.random() > 0.5)
                cell_list.append(cell)
            self.cells.append(cell_list)

    def circulate_rule(self):
        for cell_list in self.cells:
            for item in cell_list:
                item.rule()

    def circulate_nbcount(self):
        for cell_list in self.cells:
            for item in cell_list:
                item.calc_neighbour_count()


CX = 40
CY = 40
world = Grid(CX, CY)

router = APIRouter()


@router.get(
    '/get_stage',
    response_model=List[OutCell],
)
def get_stage():
    world.circulate_nbcount()
    world.circulate_rule()

    res = []
    for row in world.cells:
        for cell in row:
            res.append(
                {
                    'is_live': cell.is_live,
                    'ix': cell.ix,
                    'iy': cell.iy
                }
            )

    return res
