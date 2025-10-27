import numpy as np
from collections import deque
from config import TILE_TYPES

class LevelValidator:
    def __init__(self, level_lines):
        self.level = level_lines
        self.grid = [list(line) for line in level_lines]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.height > 0 else 0
    
    def find_tile(self, tile_char):
        positions = []
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == tile_char:
                    positions.append((i, j))
        return positions
    
    def is_walkable(self, i, j):
        if i < 0 or i >= self.height or j < 0 or j >= self.width:
            return False
        return self.grid[i][j] != '#'
    
    def bfs_connectivity(self, start_pos):
        visited = set()
        queue = deque([start_pos])
        visited.add(start_pos)
        reachable_tiles = []
        
        while queue:
            i, j = queue.popleft()
            reachable_tiles.append((i, j))
            
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ni, nj = i + di, j + dj
                if (ni, nj) not in visited and self.is_walkable(ni, nj):
                    visited.add((ni, nj))
                    queue.append((ni, nj))
        
        return reachable_tiles
    
    def check_playability(self):
        player_positions = self.find_tile('P')
        exit_positions = self.find_tile('E')
        
        if not player_positions:
            return False, "No player start position found"
        
        if not exit_positions:
            return False, "No exit found"
        
        if len(player_positions) > 1:
            return False, "Multiple player start positions"
        
        if len(exit_positions) > 1:
            return False, "Multiple exits"
        
        player_pos = player_positions[0]
        exit_pos = exit_positions[0]
        
        reachable = self.bfs_connectivity(player_pos)
        
        if exit_pos not in reachable:
            return False, "Exit is not reachable from player start"
        
        return True, "Level is playable"
    
    def check_connectivity(self):
        player_positions = self.find_tile('P')
        if not player_positions:
            return 0.0
        
        reachable = self.bfs_connectivity(player_positions[0])
        total_walkable = sum(1 for i in range(self.height) 
                           for j in range(self.width) if self.is_walkable(i, j))
        
        if total_walkable == 0:
            return 0.0
        
        return len(reachable) / total_walkable
    
    def calculate_difficulty(self):
        monsters = len(self.find_tile('M'))
        treasures = len(self.find_tile('T'))
        keys = len(self.find_tile('K'))
        doors = len(self.find_tile('D'))
        
        total_walkable = sum(1 for i in range(self.height) 
                           for j in range(self.width) if self.is_walkable(i, j))
        
        if total_walkable == 0:
            return 0.0
        
        monster_density = monsters / total_walkable
        treasure_density = treasures / total_walkable
        puzzle_score = (keys + doors) / 10.0
        
        difficulty = (monster_density * 5) + puzzle_score - (treasure_density * 2)
        
        return max(0.0, min(1.0, difficulty))
    
    def get_tile_density(self, tile_char):
        count = len(self.find_tile(tile_char))
        total_tiles = self.height * self.width
        return count / total_tiles if total_tiles > 0 else 0.0
    
    def validate_all(self):
        is_playable, message = self.check_playability()
        connectivity = self.check_connectivity()
        difficulty = self.calculate_difficulty()
        treasure_density = self.get_tile_density('T')
        monster_density = self.get_tile_density('M')
        
        return {
            'playability': is_playable,
            'playability_message': message,
            'connectivity': connectivity,
            'difficulty': difficulty,
            'treasure_density': treasure_density,
            'monster_density': monster_density
        }

