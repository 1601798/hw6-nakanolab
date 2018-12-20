class SearchProblem:
    '''探索問題を定義する抽象クラス'''
    def get_start_state(self):
        '''初期状態を返す関数'''
        raise NotImplementedError
    
    def next_states(self, state):
        '''与えられた状態 state から遷移できる状態のリストを返す関数'''
        raise NotImplementedError

    def is_goal(self, state):
        '''与えられた状態 state がゴールかどうかを True/False で返す関数'''
        raise NotImplementedError


class Maze(SearchProblem):
    def __init__(self, start_state, goal_state, maze):
        '''以下の3行は変更しないこと'''
        self.start_state = start_state
        self.goal_state = goal_state
        self.maze = maze
        # 必要に応じてこの下にコードを追加する
        self.xmax = len(maze)
        self.ymax = len(maze[0])
    
    def get_start_state(self):
        '''変更不可'''
        return self.start_state
    
    def next_states(self, state):
        '''state からたどり着くことができる座標 (x, y) のリストを返すメソッド'''
        x, y = state
        neighbors = [(x + dx, y + dy) for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
        return [(x, y) for (x, y) in neighbors
                if 0 <= x < self.xmax and 0 <= y < self.ymax and self.maze[x][y] == '.']

    def is_goal(self, state):
        '''変更不可'''
        return state == self.goal_state
    
    def show_maze(self):
        '''画面に迷路を出力するメソッド'''
        print('\n'.join(self.maze))

    def show_path(self, path):
        '''座標 (x, y) のリスト path が与えられたときに、その部分を 'o' で
           表示した迷路を画面に出力するメソッド'''
        maze = [list(row) for row in self.maze]
        for (x, y) in path:
            maze[x][y] = 'o'
        print('\n'.join(''.join(row) for row in maze))


def solve_simple_maze():
    maze = Maze((0, 0), (4, 5), ['.#####',
                                 '..#...',
                                 '#...#.',
                                 '#.###.',
                                 '#...#.'])
    assert set(maze.next_states((0, 0))) == {(1, 0)}
    assert set(maze.next_states((1, 1))) == {(1, 0), (2, 1)}

    from dfs import dfs
    path = dfs(maze)
    if path is not None:
        print('maze')
        print('----')
        maze.show_maze()
        print('\npath')
        print('----')
        maze.show_path(path)


if __name__ == '__main__':
    solve_simple_maze()
