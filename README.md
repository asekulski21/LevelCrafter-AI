# LevelCrafter-AI

Procedural Game Level Generator using Large Language Model

## Overview

This project uses TinyLlama, an open-source language model, to generate playable dungeon levels for games. The system generates ASCII-based levels and validates them using a BFS algorithm to ensure they are completable.

## Problem

Game level design is time-consuming and expensive. Traditional procedural generation algorithms often create repetitive or unplayable levels. This project explores using LLMs to generate more creative and varied levels.

## Solution

The system works in three steps:
1. **Prompt the LLM** with difficulty and level requirements
2. **Post-process** the output to fix formatting issues
3. **Validate** using BFS to ensure the exit is reachable

## Requirements

- Python 3.8+
- 8GB RAM minimum
- GPU optional (speeds up generation)

## Installation

```bash
pip install -r requirements.txt
```

First run will download the model (~2GB).

## Usage

### Interactive Mode
```bash
python main.py
```

### Demo Mode (for presentation)
```bash
python main.py demo
```

## Level Format

```
####################
#P.......##........#
#...T....##...M....#
#...#....D.........#
#................E.#
####################
```

| Symbol | Meaning |
|--------|---------|
| # | Wall |
| . | Floor |
| P | Player start |
| E | Exit |
| T | Treasure |
| M | Monster |

## Files

| File | Description |
|------|-------------|
| main.py | Entry point and demo |
| config.py | Settings and prompt |
| llm_engine.py | Model loading |
| level_generator.py | Level generation |
| validator.py | BFS playability check |
| evaluator.py | Quality metrics |
| visualizer.py | Display functions |

## Evaluation Metrics

- **Playability**: Can player reach exit (BFS check)
- **Connectivity**: Percentage of tiles reachable
- **Score**: Combined quality metric

## Results

- Playability rate: 80-90%
- Generation time: 2-10 seconds
- Levels show variety in structure

## Citations

- TinyLlama - Zhang et al. (2024)
- HuggingFace Transformers
- PyTorch
- Matplotlib

## Author

Alexander Sekulski
CSI-4130/5130 Artificial Intelligence Course Project
