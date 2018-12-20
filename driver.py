import tkinter as tk
from dfs import dfs
from maze import Maze

class MazeVisualizer:
    def __init__(self, maze, algorithm, title, grid_size=None):
        self.maze = maze
        self.algorithm = algorithm
        if grid_size:
            self.grid_size = grid_size
        else:
            self.grid_size = min(640 // maze.ymax, 480 // maze.xmax)
        self.width = self.grid_size * maze.ymax
        self.height = self.grid_size * maze.xmax
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry('%dx%d' % (self.width, self.height))
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.clear_canvas()
        self.root.bind('<Key>', self.animate)
        self.root.mainloop()
    
    def draw_box(self, coordinate, color='gray'):
        '''Only in this method, treat coordinate as (y, x).'''
        offset = 2
        (y, x) = coordinate
        self.canvas.create_rectangle(x * self.grid_size,
                                     y * self.grid_size,
                                     (x+1) * self.grid_size - offset,
                                     (y+1) * self.grid_size - offset,
                                     fill=color)
        self.canvas.update()

    def draw_path(self, path):
        for coordinate in path:
            self.draw_box(coordinate, 'orange')

    def clear_canvas(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height,
                                     fill='white')
        for x in range(self.maze.xmax):
            for y in range(self.maze.ymax):
                if self.maze.maze[x][y] == '#':
                    self.draw_box((x, y))
        self.draw_box(self.maze.start_state, 'orange')
        self.draw_box(self.maze.goal_state, 'orange')

    def animate(self, event=None):
        if event.char == 'c':
            self.clear_canvas()
        if event.char == 's':
            path = self.algorithm(self.maze)
            if path:
                self.draw_path(path)
            else:
                self.canvas.create_text(self.width // 2, self.height // 2,
                                        text='No path found!', fill='black',
                                        font=('Helvetica', 48))
        elif event.char == 'q':
            self.root.destroy()


def load_maze(filename):
    def get_xy(line):
        fields = line.split()
        return (int(fields[0]), int(fields[1]))

    with open(filename) as f:
        maze = []
        for i, line in enumerate(f):
            line = line.strip()
            if i == 0:
                start = get_xy(line)
            elif i == 1:
                goal = get_xy(line)
            elif line:
                maze.append(line)
        return Maze(start, goal, maze)

def run_simple_maze():
    maze = load_maze('simple_maze.txt')
    MazeVisualizer(maze, dfs, 'simple maze')


if __name__ == '__main__':
    run_simple_maze()