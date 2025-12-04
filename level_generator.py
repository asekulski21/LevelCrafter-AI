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
    
    # Difficulty settings: (num_treasures, num_monsters, corridor_width)
    DIFFICULTY_SETTINGS = {
        "easy": {"treasures": 5, "monsters": 2, "corridor_width": 3, "description": "wide open rooms, few monsters, many treasures"},
        "medium": {"treasures": 3, "monsters": 4, "corridor_width": 2, "description": "balanced rooms and corridors, moderate challenge"},
        "hard": {"treasures": 2, "monsters": 6, "corridor_width": 1, "description": "narrow corridors, many monsters, few treasures, maze-like"}
    }
    
    def generate(self, difficulty="medium", num_treasures=None, num_monsters=None):
        """Generate a single playable level. Retries until playable."""
        
        # Get difficulty settings
        settings = self.DIFFICULTY_SETTINGS.get(difficulty, self.DIFFICULTY_SETTINGS["medium"])
        if num_treasures is None:
            num_treasures = settings["treasures"]
        if num_monsters is None:
            num_monsters = settings["monsters"]
        
        max_attempts = 5
        
        for attempt in range(max_attempts):
            # Create the prompt
            prompt = PROMPT_TEMPLATE.format(
                difficulty=difficulty,
                width=self.width,
                height=self.height,
                num_treasures=num_treasures,
                num_monsters=num_monsters,
                difficulty_description=settings["description"]
            )
            
            # Get LLM output
            raw = self.llm.generate(prompt)
            
            # Parse and clean the output
            level = self._parse(raw)
            level = self._fix_level(level)
            
            # Fix treasure and monster counts
            level = self._fix_entity_counts(level, num_treasures, num_monsters)
            
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
        """Ensure level has exactly one player, one exit, connected floors, and walls around border."""
        grid = [list(row) for row in level]
        
        # Ensure border walls first
        for i in range(len(grid)):
            grid[i][0] = '#'
            grid[i][-1] = '#'
        for j in range(len(grid[0])):
            grid[0][j] = '#'
            grid[-1][j] = '#'
        
        # Find all P and E positions
        player_positions = []
        exit_positions = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 'P':
                    player_positions.append((i, j))
                elif grid[i][j] == 'E':
                    exit_positions.append((i, j))
        
        # Keep only one P (prefer top-left area) and convert others to floor
        if len(player_positions) > 1:
            # Sort by distance from top-left
            player_positions.sort(key=lambda p: p[0] + p[1])
            for pi, pj in player_positions[1:]:
                grid[pi][pj] = '.'
            player_positions = [player_positions[0]]
        
        # Keep only one E (prefer bottom-right area) and convert others to floor
        if len(exit_positions) > 1:
            # Sort by distance from bottom-right (descending)
            exit_positions.sort(key=lambda p: p[0] + p[1], reverse=True)
            for ei, ej in exit_positions[1:]:
                grid[ei][ej] = '.'
            exit_positions = [exit_positions[0]]
        
        # Add player if missing (top-left area)
        if not player_positions:
            for i in range(1, len(grid)-1):
                for j in range(1, len(grid[0])-1):
                    if grid[i][j] == '.':
                        grid[i][j] = 'P'
                        player_positions = [(i, j)]
                        break
                else:
                    continue
                break
        
        # Add exit if missing (bottom-right area)
        if not exit_positions:
            for i in range(len(grid)-2, 0, -1):
                for j in range(len(grid[0])-2, 0, -1):
                    if grid[i][j] == '.':
                        grid[i][j] = 'E'
                        exit_positions = [(i, j)]
                        break
                else:
                    continue
                break
        
        # Connect all floor regions to ensure playability
        grid = self._connect_all_floors(grid)
        
        # Final check - carve path from P to E if still not connected
        level = [''.join(row) for row in grid]
        validator = LevelValidator(level)
        playable, _ = validator.is_playable()
        
        if not playable:
            grid = [list(row) for row in level]
            grid = self._carve_path(grid)
        
        return [''.join(row) for row in grid]
    
    def _fix_entity_counts(self, level, target_treasures, target_monsters):
        """Ensure level has the correct number of treasures and monsters."""
        import random
        
        grid = [list(row) for row in level]
        height = len(grid)
        width = len(grid[0])
        
        # Find current positions
        treasures = []
        monsters = []
        floors = []
        player_pos = None
        exit_pos = None
        
        for i in range(height):
            for j in range(width):
                if grid[i][j] == 'T':
                    treasures.append((i, j))
                elif grid[i][j] == 'M':
                    monsters.append((i, j))
                elif grid[i][j] == '.':
                    floors.append((i, j))
                elif grid[i][j] == 'P':
                    player_pos = (i, j)
                elif grid[i][j] == 'E':
                    exit_pos = (i, j)
        
        # Remove excess treasures
        while len(treasures) > target_treasures:
            ti, tj = treasures.pop()
            grid[ti][tj] = '.'
            floors.append((ti, tj))
        
        # Remove excess monsters
        while len(monsters) > target_monsters:
            mi, mj = monsters.pop()
            grid[mi][mj] = '.'
            floors.append((mi, mj))
        
        # Filter floors to avoid placing near P or E
        safe_floors = []
        for (i, j) in floors:
            dist_to_p = abs(i - player_pos[0]) + abs(j - player_pos[1]) if player_pos else 999
            dist_to_e = abs(i - exit_pos[0]) + abs(j - exit_pos[1]) if exit_pos else 999
            if dist_to_p > 2 and dist_to_e > 2:
                safe_floors.append((i, j))
        
        random.shuffle(safe_floors)
        
        # Add missing treasures
        while len(treasures) < target_treasures and safe_floors:
            ti, tj = safe_floors.pop()
            grid[ti][tj] = 'T'
            treasures.append((ti, tj))
        
        # Add missing monsters
        while len(monsters) < target_monsters and safe_floors:
            mi, mj = safe_floors.pop()
            grid[mi][mj] = 'M'
            monsters.append((mi, mj))
        
        return [''.join(row) for row in grid]
    
    def _connect_all_floors(self, grid):
        """Connect all separate floor regions into one connected area."""
        height = len(grid)
        width = len(grid[0])
        
        def get_walkable_neighbors(i, j):
            neighbors = []
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i + di, j + dj
                if 0 < ni < height-1 and 0 < nj < width-1:
                    if grid[ni][nj] != '#':
                        neighbors.append((ni, nj))
            return neighbors
        
        def flood_fill(start, visited):
            """Find all tiles connected to start."""
            region = set()
            stack = [start]
            while stack:
                pos = stack.pop()
                if pos in visited:
                    continue
                visited.add(pos)
                region.add(pos)
                i, j = pos
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 < ni < height-1 and 0 < nj < width-1:
                        if grid[ni][nj] != '#' and (ni, nj) not in visited:
                            stack.append((ni, nj))
            return region
        
        # Find all separate floor regions
        visited = set()
        regions = []
        for i in range(1, height-1):
            for j in range(1, width-1):
                if grid[i][j] != '#' and (i, j) not in visited:
                    region = flood_fill((i, j), visited)
                    regions.append(region)
        
        if len(regions) <= 1:
            return grid  # Already connected or no floors
        
        # Find which region contains the player
        player_region_idx = 0
        for idx, region in enumerate(regions):
            for i, j in region:
                if grid[i][j] == 'P':
                    player_region_idx = idx
                    break
        
        # Connect all other regions to the player's region
        main_region = regions[player_region_idx]
        
        for idx, region in enumerate(regions):
            if idx == player_region_idx:
                continue
            
            # Find closest points between main_region and this region
            min_dist = float('inf')
            best_main = None
            best_other = None
            
            for mi, mj in main_region:
                for oi, oj in region:
                    dist = abs(mi - oi) + abs(mj - oj)
                    if dist < min_dist:
                        min_dist = dist
                        best_main = (mi, mj)
                        best_other = (oi, oj)
            
            # Carve a path between them
            if best_main and best_other:
                mi, mj = best_main
                oi, oj = best_other
                
                # Move horizontally first
                j = mj
                while j != oj:
                    if grid[mi][j] == '#':
                        grid[mi][j] = '.'
                    j += 1 if oj > mj else -1
                
                # Then move vertically
                i = mi
                while i != oi:
                    if grid[i][oj] == '#':
                        grid[i][oj] = '.'
                    i += 1 if oi > mi else -1
                
                # Add all tiles from this region to main_region
                main_region = main_region.union(region)
        
        return grid
    
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
        import random
        
        # Start with all walls
        grid = [['#' for _ in range(self.width)] for _ in range(self.height)]
        
        settings = self.DIFFICULTY_SETTINGS.get(difficulty, self.DIFFICULTY_SETTINGS["medium"])
        corridor_width = settings["corridor_width"]
        
        if difficulty == "easy":
            # Easy: Large open rooms with wide corridors
            # Create two big rooms connected by wide corridor
            # Left room
            for i in range(2, self.height - 2):
                for j in range(2, self.width // 2 - 1):
                    grid[i][j] = '.'
            # Right room
            for i in range(2, self.height - 2):
                for j in range(self.width // 2 + 2, self.width - 2):
                    grid[i][j] = '.'
            # Wide connecting corridor (3 tiles wide)
            for i in range(self.height // 2 - 1, self.height // 2 + 2):
                for j in range(self.width // 2 - 1, self.width // 2 + 3):
                    grid[i][j] = '.'
                    
        elif difficulty == "medium":
            # Medium: Multiple rooms with 2-wide corridors
            # Top-left room
            for i in range(2, self.height // 2):
                for j in range(2, self.width // 2 - 1):
                    grid[i][j] = '.'
            # Top-right room
            for i in range(2, self.height // 2):
                for j in range(self.width // 2 + 2, self.width - 2):
                    grid[i][j] = '.'
            # Bottom room (spans width)
            for i in range(self.height // 2 + 2, self.height - 2):
                for j in range(2, self.width - 2):
                    grid[i][j] = '.'
            # Horizontal corridor connecting top rooms
            for i in range(self.height // 2 - 2, self.height // 2):
                for j in range(self.width // 2 - 1, self.width // 2 + 3):
                    grid[i][j] = '.'
            # Vertical corridors to bottom room
            for i in range(self.height // 2, self.height // 2 + 3):
                grid[i][4] = '.'
                grid[i][5] = '.'
                grid[i][self.width - 5] = '.'
                grid[i][self.width - 6] = '.'
                
        else:  # hard
            # Hard: Maze-like with narrow single-tile corridors
            # Create a winding path with small rooms
            # Small starting room
            for i in range(2, 5):
                for j in range(2, 5):
                    grid[i][j] = '.'
            # Narrow corridor going right
            for j in range(5, self.width - 5):
                grid[3][j] = '.'
            # Narrow corridor going down
            for i in range(3, self.height - 4):
                grid[i][self.width - 6] = '.'
            # Narrow corridor going left
            for j in range(5, self.width - 5):
                grid[self.height - 5][j] = '.'
            # Narrow corridor going down to exit room
            for i in range(self.height - 5, self.height - 2):
                grid[i][5] = '.'
            # Small exit room
            for i in range(self.height - 4, self.height - 2):
                for j in range(self.width - 5, self.width - 2):
                    grid[i][j] = '.'
            # Connect to exit room
            for j in range(5, self.width - 4):
                grid[self.height - 3][j] = '.'
        
        # Place player (top-left area)
        grid[2][2] = 'P'
        
        # Place exit (bottom-right area)
        grid[self.height - 3][self.width - 3] = 'E'
        
        # Collect all valid floor positions (not P, E, or #)
        floor_spots = []
        for i in range(2, self.height - 2):
            for j in range(2, self.width - 2):
                if grid[i][j] == '.':
                    # Avoid placing too close to P or E
                    dist_to_p = abs(i - 2) + abs(j - 2)
                    dist_to_e = abs(i - (self.height - 3)) + abs(j - (self.width - 3))
                    if dist_to_p > 2 and dist_to_e > 2:
                        floor_spots.append((i, j))
        
        random.shuffle(floor_spots)
        
        # Place treasures
        for idx in range(min(num_treasures, len(floor_spots))):
            ti, tj = floor_spots[idx]
            grid[ti][tj] = 'T'
        
        # Place monsters (after treasures)
        remaining_spots = floor_spots[num_treasures:]
        for idx in range(min(num_monsters, len(remaining_spots))):
            mi, mj = remaining_spots[idx]
            grid[mi][mj] = 'M'
        
        return [''.join(row) for row in grid]
