import glob
import os
import sys
import time
import tkinter as tk
from dfs import dfs
from maze import Maze

class MazeVisualizer:
    def __init__(self, maze, algorithm, title, grid_size=None):
        self.maze = maze
        self.algorithm = algorithm
        self.routes = []
        self.route_id = 0
        if grid_size:
            self.grid_size = grid_size
        else:
            self.grid_size = min(1200 // maze.ymax, 680 // maze.xmax)
        self.width = self.grid_size * maze.ymax
        self.height = self.grid_size * maze.xmax
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry('%dx%d' % (self.width, self.height))
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        text = '%s\n(%d x %d)' % (title, maze.ymax, maze.xmax)
        self.canvas.create_text(self.width // 2, self.height // 2,
                                text=text, fill='black', justify=tk.CENTER,
                                font=('Helvetica', 48))
        self.root.bind('<Key>', self.animate)
        self.root.mainloop()
    
    def draw_box(self, coordinate, color='gray', update=False):
        '''Only in this method, treat coordinate as (y, x).'''
        offset = 1
        (y, x) = coordinate
        self.canvas.create_rectangle(x * self.grid_size,
                                     y * self.grid_size,
                                     (x+1) * self.grid_size - offset,
                                     (y+1) * self.grid_size - offset,
                                     fill=color, outline=color)
        if update:
            self.canvas.update()

    def draw_route(self, route):
        for coordinate in route:
            self.draw_box(coordinate, 'orange', True)
    
    def draw_next_route(self):
        self.draw_route(self.routes[self.route_id])
        if len(self.routes) > 1:
            self.canvas.create_text(self.width // 2, self.height // 2,
                                    text='#%d' % (self.route_id + 1),
                                    fill='red', font=('Helvetica', 64))
        self.route_id = (self.route_id + 1) % len(self.routes)

    def clear_canvas(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height,
                                     fill='black')
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
            if not self.routes:
                self.routes = self.algorithm(self.maze)
            if self.routes:
                self.draw_next_route()
            else:
                self.canvas.create_text(self.width // 2, self.height // 2,
                                        text='No route found!', fill='red',
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

def view_maze(title, filename):
    try:
        maze = load_maze(filename)
    except Exception as e:
        print('Error loading %s: %s' % (filename, e))
        return
    try:
        MazeVisualizer(maze, dfs, title)
    except Exception as e:
        print('Error viewing %s: %s' % (filename, e))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filenames = sorted(glob.glob('%s/*/maze.txt' % sys.argv[1]))
        for filename in filenames:
            print(filename)
            title = filename.split(os.sep)[-2]
            view_maze(title, filename)
    else:
        view_maze('My maze', 'maze.txt')