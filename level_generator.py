import random
import numpy as np
from llm_engine import LLMEngine
from config import PROMPT_TEMPLATE, LEVEL_WIDTH, LEVEL_HEIGHT, TILE_TYPES

class LevelGenerator:
    def __init__(self):
        self.llm = LLMEngine()
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT
    
    def create_prompt(self, difficulty="medium", num_treasures=3, num_monsters=5):
        prompt = PROMPT_TEMPLATE.format(
            difficulty=difficulty,
            width=self.width,
            height=self.height,
            num_treasures=num_treasures,
            num_monsters=num_monsters
        )
        return prompt
    
    def parse_level(self, raw_output):
        lines = raw_output.strip().split('\n')
        level_lines = []
        
        for line in lines:
            clean_line = ''.join(c for c in line if c in TILE_TYPES.keys())
            if clean_line and len(clean_line) > 0:
                level_lines.append(clean_line)
        
        if len(level_lines) < self.height:
            level_lines.extend(['#' * self.width] * (self.height - len(level_lines)))
        
        level_lines = level_lines[:self.height]
        
        normalized_lines = []
        for line in level_lines:
            if len(line) < self.width:
                line = line + '#' * (self.width - len(line))
            else:
                line = line[:self.width]
            normalized_lines.append(line)
        
        return normalized_lines
    
    def post_process_level(self, level_lines):
        grid = [list(line) for line in level_lines]
        
        has_player = any('P' in line for line in grid)
        has_exit = any('E' in line for line in grid)
        
        if not has_player:
            for i in range(1, len(grid) - 1):
                for j in range(1, len(grid[0]) - 1):
                    if grid[i][j] == '.':
                        grid[i][j] = 'P'
                        has_player = True
                        break
                if has_player:
                    break
        
        if not has_exit:
            for i in range(len(grid) - 2, 0, -1):
                for j in range(len(grid[0]) - 2, 0, -1):
                    if grid[i][j] == '.':
                        grid[i][j] = 'E'
                        has_exit = True
                        break
                if has_exit:
                    break
        
        for i in range(len(grid)):
            grid[i][0] = '#'
            grid[i][-1] = '#'
        for j in range(len(grid[0])):
            grid[0][j] = '#'
            grid[-1][j] = '#'
        
        return [''.join(row) for row in grid]
    
    def generate(self, difficulty="medium", num_treasures=3, num_monsters=5):
        prompt = self.create_prompt(difficulty, num_treasures, num_monsters)
        
        raw_output = self.llm.generate_level(prompt)
        
        level_lines = self.parse_level(raw_output)
        
        level_lines = self.post_process_level(level_lines)
        
        return level_lines
    
    def generate_multiple(self, count=5, difficulty="medium"):
        levels = []
        for i in range(count):
            print(f"Generating level {i+1}/{count}...")
            level = self.generate(
                difficulty=difficulty,
                num_treasures=random.randint(2, 5),
                num_monsters=random.randint(3, 7)
            )
            levels.append(level)
        return levels

