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
You are a game level designer. Generate ASCII dungeon levels.</s>
<|user|>
Create a {difficulty} difficulty dungeon level ({width}x{height}).
Use: # for walls, . for floor, P for player start, E for exit, T for treasure, M for monster.
Include {num_treasures} treasures and {num_monsters} monsters.
Output only the level grid:</s>
<|assistant|>
"""
