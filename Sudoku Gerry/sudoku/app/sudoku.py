import numpy as np

class Sudoku:
    def __init__(self, grid):
        self.grid = np.array(grid)
        self.original = self.grid.copy()
    
    def is_valid(self, row, col, num):
        # Verificar fila
        if num in self.grid[row]:
            return False
        
        # Verificar columna
        if num in self.grid[:, col]:
            return False
        
        # Verificar subcuadrícula 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        
        return True
    
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None
    
    def get_solution(self):
        return self.grid

class Solver:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.steps_taken = 0
        self.nodes_explored = 0
    
    def solve(self):
        self.steps_taken = 0
        self.nodes_explored = 0
        return self._solve()
    
    def _solve(self):
        self.nodes_explored += 1
        empty = self.sudoku.find_empty()
        
        if not empty:
            return True
        
        row, col = empty
        
        for num in range(1, 10):
            self.steps_taken += 1
            
            if self.sudoku.is_valid(row, col, num):
                self.sudoku.grid[row][col] = num
                
                if self._solve():
                    return True
                
                self.sudoku.grid[row][col] = 0
        
        return False
    
    def get_statistics(self):
        return {
            'steps_taken': self.steps_taken,
            'nodes_explored': self.nodes_explored
        }
    
    def get_solution(self):
        return self.sudoku.get_solution() 