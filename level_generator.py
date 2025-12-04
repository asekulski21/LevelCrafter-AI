# Level Generator - creates dungeon levels using the LLM

from llm_engine import LLMEngine
from validator import LevelValidator
from config import PROMPT_TEMPLATE, LEVEL_WIDTH, LEVEL_HEIGHT, TILES

class LevelGenerator:
    """Generates game levels using the LLM."""
    
    def __init__(self):
        self.llm = LLMEngine()
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT
    
    def generate(self, difficulty="medium", num_treasures=3, num_monsters=4):
        """Generate a single playable level. Retries until playable."""
        
        max_attempts = 5
        
        for attempt in range(max_attempts):
            # Create the prompt
            prompt = PROMPT_TEMPLATE.format(
                difficulty=difficulty,
                width=self.width,
                height=self.height,
                num_treasures=num_treasures,
                num_monsters=num_monsters
            )
            
            # Get LLM output
            raw = self.llm.generate(prompt)
            
            # Parse and clean the output
            level = self._parse(raw)
            level = self._fix_level(level)
            
            # Check if playable
            validator = LevelValidator(level)
            playable, _ = validator.is_playable()
            
            if playable:
                return level
            
            print(f"  Attempt {attempt + 1} not playable, retrying...")
        
        # If all attempts failed, force a playable level
        print("  Creating guaranteed playable level...")
        level = self._create_fallback_level(difficulty, num_treasures, num_monsters)
        return level
    
    def _parse(self, raw):
        """Extract valid level characters from LLM output."""
        lines = []
        for line in raw.strip().split('\n'):
            clean = ''.join(c for c in line if c in TILES)
            if clean:
                lines.append(clean)
        
        # Ensure correct dimensions
        while len(lines) < self.height:
            lines.append('#' * self.width)
        lines = lines[:self.height]
        
        # Normalize width
        result = []
        for line in lines:
            if len(line) < self.width:
                line = line + '#' * (self.width - len(line))
            result.append(line[:self.width])
        
        return result
    
    def _fix_level(self, level):
        """Ensure level has player, exit, and walls around border."""
        grid = [list(row) for row in level]
        
        # Add player if missing (top-left area)
        if not any('P' in row for row in grid):
            for i in range(1, len(grid)-1):
                for j in range(1, len(grid[0])-1):
                    if grid[i][j] == '.':
                        grid[i][j] = 'P'
                        break
                else:
                    continue
                break
        
        # Add exit if missing (bottom-right area)
        if not any('E' in row for row in grid):
            for i in range(len(grid)-2, 0, -1):
                for j in range(len(grid[0])-2, 0, -1):
                    if grid[i][j] == '.':
                        grid[i][j] = 'E'
                        break
                else:
                    continue
                break
        
        # Ensure border walls
        for i in range(len(grid)):
            grid[i][0] = '#'
            grid[i][-1] = '#'
        for j in range(len(grid[0])):
            grid[0][j] = '#'
            grid[-1][j] = '#'
        
        # Try to create path if not playable
        level = [''.join(row) for row in grid]
        validator = LevelValidator(level)
        playable, _ = validator.is_playable()
        
        if not playable:
            grid = self._carve_path(grid)
        
        return [''.join(row) for row in grid]
    
    def _carve_path(self, grid):
        """Carve a path from player to exit to ensure playability."""
        # Find player and exit positions
        player_pos = None
        exit_pos = None
        
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 'P':
                    player_pos = (i, j)
                elif grid[i][j] == 'E':
                    exit_pos = (i, j)
        
        if not player_pos or not exit_pos:
            return grid
        
        # Carve horizontal then vertical path
        pi, pj = player_pos
        ei, ej = exit_pos
        
        # Move horizontally first
        j = pj
        while j != ej:
            if grid[pi][j] == '#':
                grid[pi][j] = '.'
            j += 1 if ej > pj else -1
        
        # Then move vertically
        i = pi
        while i != ei:
            if grid[i][ej] == '#':
                grid[i][ej] = '.'
            i += 1 if ei > pi else -1
        
        # Make sure player and exit are still there
        grid[player_pos[0]][player_pos[1]] = 'P'
        grid[exit_pos[0]][exit_pos[1]] = 'E'
        
        return grid
    
    def _create_fallback_level(self, difficulty, num_treasures, num_monsters):
        """Create a guaranteed playable level if LLM fails."""
        # Start with all walls
        grid = [['#' for _ in range(self.width)] for _ in range(self.height)]
        
        # Create open area in the middle
        for i in range(2, self.height - 2):
            for j in range(2, self.width - 2):
                grid[i][j] = '.'
        
        # Add some walls based on difficulty
        if difficulty == "medium":
            for i in range(3, self.height - 3):
                grid[i][self.width // 2] = '#'
            grid[self.height // 2][self.width // 2] = '.'  # Opening
        elif difficulty == "hard":
            for i in range(3, self.height - 3):
                grid[i][self.width // 3] = '#'
                grid[i][2 * self.width // 3] = '#'
            grid[self.height // 2][self.width // 3] = '.'
            grid[self.height // 2][2 * self.width // 3] = '.'
        
        # Place player (top-left)
        grid[2][2] = 'P'
        
        # Place exit (bottom-right)
        grid[self.height - 3][self.width - 3] = 'E'
        
        # Place treasures
        treasure_spots = [(3, 5), (4, 10), (self.height-4, 5), (3, self.width-5), (self.height-4, self.width-6)]
        for idx in range(min(num_treasures, len(treasure_spots))):
            ti, tj = treasure_spots[idx]
            if grid[ti][tj] == '.':
                grid[ti][tj] = 'T'
        
        # Place monsters
        monster_spots = [(4, 7), (self.height-4, 8), (5, self.width-5), (self.height-5, 4), (3, 12)]
        for idx in range(min(num_monsters, len(monster_spots))):
            mi, mj = monster_spots[idx]
            if grid[mi][mj] == '.':
                grid[mi][mj] = 'M'
        
        return [''.join(row) for row in grid]
