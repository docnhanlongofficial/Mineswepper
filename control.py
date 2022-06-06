import random
from queue import Queue
from tkinter import Label
from components import Grid, Panel, Cell
from threading import Thread
from typing import Dict

WIDTH = 16
TOTAL_BOM_NUM = 2*WIDTH
BOM_SYMBOL = '*'
EMPTY_SYMBOL = ' '

class GridControl:

    def __init__(self, grid: Grid):
        self.grid = grid
        self.game_over = False        

    def generate_matrix(self, width, element):
        return [[element for _ in range(width)] for _ in range(width)]

    def print_matrix(self, matrix):
        for e, row in enumerate(matrix):
            if e == 0:
                print(f" {[str(i) for i in range(WIDTH)]}")
            print(f"{e}{row}")


    def random_bomb(self,bom_num):
        bom_pos = set()
        while len(bom_pos) < bom_num:
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, WIDTH)
            bom_pos.add((x, y))
        return bom_pos


    def locate_surround(self, x, y, width):
        """
            return surround locations of a given location (x,y) in a matrix that has a width of 'width'
        """
        surround_loc = {(x+1, y), (x, y+1), 
                    (x-1, y), (x, y-1), 
                    (x+1, y+1), (x-1, y-1),
                    (x+1, y-1), (x-1, y+1)}
        # when given loc at the first row
        if x == 0:
            surround_loc.discard((x-1, y))
            surround_loc.discard((x-1, y-1))
            surround_loc.discard((x-1, y+1))
        # at the final row
        if x == width - 1:
            surround_loc.discard((x+1, y))
            surround_loc.discard((x+1, y+1))
            surround_loc.discard((x+1, y-1))
        # at the first col
        if y == 0:
            surround_loc.discard((x, y-1))
            surround_loc.discard((x-1, y-1))
            surround_loc.discard((x+1, y-1))
        # at the final col
        if y == width-1:
            surround_loc.discard((x, y+1))
            surround_loc.discard((x+1, y+1))
            surround_loc.discard((x-1, y+1))
        return surround_loc


    def assign_bombs(self, matrix):
        """
            assign bombs to random location of the given matrix
        """
        bom_pos = self.random_bomb(TOTAL_BOM_NUM)
        for pos in list(bom_pos):
            x = pos[0]
            y = pos[1]
            matrix[x][y] = BOM_SYMBOL


    def assign_bomb_num(self, matrix):
        """
            after assigning random bombs, fill the number of surround bombs of each cell in matrix
        """
        for row in range(WIDTH):
            for e in range(WIDTH):
                # skip bom cell
                if matrix[row][e] == BOM_SYMBOL:
                    continue
                bom_num = 0
                for loc in self.locate_surround(row, e, WIDTH):
                    if matrix[loc[0]][loc[1]] == BOM_SYMBOL:
                        bom_num += 1
                matrix[row][e] = str(bom_num)


    def get_orthogonal_neighbor_locations(self, x, y, width):
        """
            return surround locations of a given location (x,y) in a matrix that has a width of 'width'
        """
        surround_loc = {(x+1, y), (x, y+1),
                    (x-1, y), (x, y-1),
                    (x+1, y-1), (x-1, y+1)}
        # when given loc at the first row
        if x == 0:
            surround_loc.discard((x-1, y))
            surround_loc.discard((x-1, y+1))
        # at the final row
        if x == width - 1:
            surround_loc.discard((x+1, y))
            surround_loc.discard((x+1, y-1))
        # at the first col
        if y == 0:
            surround_loc.discard((x, y-1))
            surround_loc.discard((x+1, y-1))
        # at the final col
        if y == width-1:
            surround_loc.discard((x, y+1))
            surround_loc.discard((x-1, y+1))
        return surround_loc

    def binding_click_event_to_cells(self, cells):
        for row in cells:
            for cell in row:
                cell.label.bind('<Button-1>', lambda event, args={'x': cell.x, 'y': cell.y}: self.start_open_cell(event, args))

    def open_all_neighbors_of_empty_cell(self, x: int, y: int):
        surround_loc = self.get_orthogonal_neighbor_locations(x, y, WIDTH)
        for loc in surround_loc:
            self.grid.cells[loc[0]][loc[1]].reveal()

    def flood_fill(self, selected_loc: Dict[str, int]):
        """
            breath first search
        """

        x = selected_loc['x']
        y = selected_loc['y']
        cell_queue = Queue(maxsize=WIDTH**2)
        cell_queue.put((x, y))

        # a 2D matrix that represents opening status of the cells
        visited_cells = self.generate_matrix(WIDTH, False)
        
        while not cell_queue.empty():

            current_cell = cell_queue.get()
            x, y = current_cell[0], current_cell[1]

            # reveal the current cell
            self.grid.cells[x][y].reveal()
            # mark current cell as opened
            visited_cells[x][y] = True
            self.open_all_neighbors_of_empty_cell(x, y)
            
            # visit all neighbors of the current cell    
            surround_loc = self.get_orthogonal_neighbor_locations(x, y, WIDTH)
            for loc in surround_loc:
                surround_x, surround_y = loc[0], loc[1]
                # if neighbor is empty and not opened
                if self.grid.get_cell_value(surround_x, surround_y) == '0' and \
                        visited_cells[surround_x][surround_y] is False:
                    cell_queue.put(loc)

    def open_cell(self, event, loc):
        x, y = loc['x'], loc['y']
        if self.grid.get_cell_value(x, y) == BOM_SYMBOL:
            self.grid.cells[x][y].reveal()
            # stop game
            self.grid.remove_all_events()
            self.game_over = True
            return -1
        elif self.grid.get_cell_value(x, y) != '0':
            self.grid.cells[x][y].reveal()
            return 1
        else:
            self.flood_fill(selected_loc={'x': x, 'y': y})
            return 1
    
    # using thread to avoid Tkinter freeze
    def start_open_cell(self, event, loc):
        Thread(target=self.open_cell, args=(event, loc)).start()


class FlagControl:
    
    def __init__(self, grid: Grid, panel: Panel, num_flags: int):
        self.grid = grid
        self.panel = panel
        self.num_flags = num_flags
        self.is_flagged = [[False for i in range(self.grid.width)] for j in range(self.grid.width)]

        self.bind_event_to_cell()
        
    
    def bind_event_to_cell(self):
        # bind control function to each cell
        for row in self.grid.cells:
            for cell in row:
                cell.label.bind(
                    '<Button-3>', 
                    lambda event, args={'x': cell.x, 'y': cell.y}: self.change(event, args),
                    add='+')

    def flagging(self, x, y):
        if self.is_flagged[x][y] == True:
            self.is_flagged[x][y] = False
        else:
            self.is_flagged[x][y] = True

    def change(self, event, loc: dict):
        
        x, y = loc['x'], loc['y']
        
        if self.grid.is_opened(x, y):
            return

        cell = self.grid.cells[x][y]        
        prev_num_flags = self.num_flags

        if self.is_flagged[x][y] == False:
            self.num_flags -= 1
        else:
            self.num_flags += 1

        if self.num_flags < 0:
            self.num_flags = 0
        elif self.num_flags > self.panel.total_bom_num:
            self.num_flags = self.panel.total_bom_num

        if prev_num_flags != self.num_flags:  
            self.flagging(x, y) 
            cell.flagged()
            self.panel.change_display_num(self.num_flags)
        
        # check whether all bombs are flagged
        if self.num_flags == 0:
            is_win = True
            for i in range(self.grid.width):
                for j in range(self.grid.width):
                    if self.is_flagged[i][j] == True and self.grid.cells[i][j].value != BOM_SYMBOL:
                        is_win = False
            if is_win == True:
                self.grid.remove_all_events()
                # display "You win" on the panel
                self.panel.flag_container.pack_forget()
                self.panel.display_num.pack_forget()
                self.panel.undo_button.pack_forget()
                win_label = Label(self.panel.panel, text=f'You Win', font=('Arial', 20))
                win_label.pack()
            

    def set_num_flags(self, num_flags):
        self.num_flags = num_flags


class CellUndoThread(Thread):
    def __init__(self, cell: Cell):
        super().__init__()
        self.cell = cell

    def run(self):
        self.cell.back()

class UndoControl:
    def __init__(self, grid: Grid, panel: Panel, grid_control: GridControl, flag_control: FlagControl) -> None:
        self.grid = grid
        self.panel = panel
        self.grid_control = grid_control
        self.flag_control = flag_control
        self.panel.undo_button.bind('<Button-1>', self.undo)

    def undo(self, event):
        for row in self.grid.cells:
            for cell in row:
                if cell.value == BOM_SYMBOL:
                    CellUndoThread(cell).start()
        if self.grid_control.game_over is True:
            self.grid_control.binding_click_event_to_cells(self.grid.cells)
            self.flag_control.bind_event_to_cell()

