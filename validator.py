# Level Validator - checks if levels are playable using BFS

from collections import deque

class LevelValidator:
    """Validates that a level is playable using Breadth-First Search."""
    
    def __init__(self, level):
        self.grid = [list(row) for row in level]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
    
    def find_tile(self, char):
        """Find position of a tile."""
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == char:
                    return (i, j)
        return None
    
    def is_walkable(self, i, j):
        """Check if position is walkable (not a wall)."""
        if 0 <= i < self.height and 0 <= j < self.width:
            return self.grid[i][j] != '#'
        return False
    
    def bfs(self, start):
        """
        Breadth-First Search to find all reachable tiles.
        
        This algorithm explores the level layer by layer,
        starting from the player position. It uses a queue
        to process tiles in order of distance from start.
        """
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            i, j = queue.popleft()
            
            # Check 4 directions: up, down, left, right
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i + di, j + dj
                if (ni, nj) not in visited and self.is_walkable(ni, nj):
                    visited.add((ni, nj))
                    queue.append((ni, nj))
        
        return visited
    
    def is_playable(self):
        """Check if player can reach exit."""
        player = self.find_tile('P')
        exit_tile = self.find_tile('E')
        
        if not player:
            return False, "No player start"
        if not exit_tile:
            return False, "No exit"
        
        reachable = self.bfs(player)
        
        if exit_tile in reachable:
            return True, "Playable"
        else:
            return False, "Exit not reachable"
    
    def get_connectivity(self):
        """Calculate what percentage of floor tiles are reachable."""
        player = self.find_tile('P')
        if not player:
            return 0.0
        
        reachable = self.bfs(player)
        total_walkable = sum(1 for i in range(self.height) 
                           for j in range(self.width) 
                           if self.is_walkable(i, j))
        
        return len(reachable) / total_walkable if total_walkable > 0 else 0.0

