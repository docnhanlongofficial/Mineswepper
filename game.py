from tkinter import BOTTOM, Tk, Frame, PhotoImage, RAISED
from control import BOM_SYMBOL, WIDTH, TOTAL_BOM_NUM
from control import GridControl, UndoControl, FlagControl
from components import Grid, Panel, Cell

class Game:
    def __init__(self, window: Tk, ) -> None:
        
        self.window = window

        self.panel = Panel(self.window, total_bom_num=TOTAL_BOM_NUM)

        # to wrap the grid of cell
        self.frame = Frame(self.window, bd=5, relief=RAISED)
        self.frame.pack(side=BOTTOM)

        self.grid = Grid (wrapper=self.frame, width=WIDTH)

        self.cells = [[None for i in range(WIDTH)] for j in range(WIDTH)]
        
        

        self.grid_control = GridControl(self.grid)
        self.matrix = self.grid_control.generate_matrix(WIDTH, None)
        self.grid_control.assign_bombs(self.matrix)
        self.grid_control.assign_bomb_num(self.matrix)
        self.grid_control.print_matrix(self.matrix)

        # creating and adding cells to the grid
        for i in range(WIDTH):
            for j in range(WIDTH):
                self.cells[i][j] = Cell(wrapper=self.frame, x=i, y=j, value=self.matrix[i][j], bom_symbol=BOM_SYMBOL)
                self.grid.add_cell(cell=self.cells[i][j], x=i, y=j)
        
        self.grid_control.binding_click_event_to_cells(self.cells)

        self.flagControl = FlagControl(grid=self.grid, panel=self.panel, num_flags=TOTAL_BOM_NUM)
        
        UndoControl(grid=self.grid, panel=self.panel, grid_control=self.grid_control, flag_control=self.flagControl)
        
    def start(self):
        self.window.mainloop()
    def quit(self):
        self.window.quit()


# to stop the program when the window is closed
def destroy_game():
    print('Quit')
    window.quit()
    window.destroy()
    
window = Tk()
window.protocol("WM_DELETE_WINDOW", destroy_game)
window.title('Minesweeper')
# change icon image of the window
icon = PhotoImage(file='images//bomb.png')
window.iconphoto(True, icon)
game = Game(window=window)
game.start()
