# Configuration for the Level Generator

import torch

# Model settings
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Generation settings
MAX_TOKENS = 512
TEMPERATURE = 0.8

# Level settings
LEVEL_WIDTH = 20
LEVEL_HEIGHT = 12

# Valid tiles
TILES = ['#', '.', 'P', 'E', 'T', 'M', 'K', 'D']

# Prompt for the LLM
PROMPT_TEMPLATE = """<|system|>
You are a dungeon level designer. Create unique ASCII game levels.</s>
<|user|>
Generate a {difficulty} dungeon level, exactly {width} characters wide and {height} rows tall.
Style: {difficulty_description}

Tiles: # wall, . floor, P player, E exit, T treasure, M monster

Requirements:
- {width} characters per row, {height} rows total
- # border on all edges
- 1 P top-left area, 1 E bottom-right area
- {num_treasures} T and {num_monsters} M scattered throughout
- Floors and corridors spread across ENTIRE level (left, middle, AND right sides)
- Connected path from P to E

Generate a unique {difficulty} level now:</s>
<|assistant|>
"""
