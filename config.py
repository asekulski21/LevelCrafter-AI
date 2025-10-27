import torch

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.8
TOP_P = 0.95
TOP_K = 50

LEVEL_WIDTH = 20
LEVEL_HEIGHT = 12

TILE_TYPES = {
    '#': 'wall',
    '.': 'floor',
    'P': 'player_start',
    'E': 'exit',
    'T': 'treasure',
    'M': 'monster',
    'K': 'key',
    'D': 'door',
    ' ': 'empty'
}

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

EVALUATION_METRICS = [
    'playability',
    'connectivity',
    'difficulty',
    'diversity',
    'treasure_density',
    'monster_density'
]

PROMPT_TEMPLATE = """<|system|>
You are a game level designer AI. Generate ASCII-based dungeon levels that are playable and engaging.</s>
<|user|>
Create a {difficulty} difficulty dungeon level with dimensions {width}x{height}.
The level should include:
- One player start position (P)
- One exit (E)
- Walls (#) forming corridors and rooms
- Floor tiles (.)
- {num_treasures} treasures (T)
- {num_monsters} monsters (M)
- Optional keys (K) and doors (D)

Generate only the level grid, no explanation:</s>
<|assistant|>
"""

