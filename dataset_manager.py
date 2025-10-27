import os
import json
import random
from datetime import datetime

class DatasetManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.examples_dir = os.path.join(data_dir, "examples")
        self.generated_dir = os.path.join(data_dir, "generated")
        self.ensure_directories()
        self.create_seed_examples()
    
    def ensure_directories(self):
        os.makedirs(self.examples_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)
    
    def create_seed_examples(self):
        examples = [
            {
                "name": "simple_corridor",
                "difficulty": "easy",
                "level": [
                    "####################",
                    "#P................E#",
                    "#.....T...M........#",
                    "#..................#",
                    "####################",
                    "####################",
                    "####################",
                    "####################",
                    "####################",
                    "####################",
                    "####################",
                    "####################"
                ]
            },
            {
                "name": "room_and_hallway",
                "difficulty": "medium",
                "level": [
                    "####################",
                    "#P.......##........#",
                    "#...T....##...M....#",
                    "#...#....##........#",
                    "#...#....D.........#",
                    "#...#....##........#",
                    "#K..#....##...T....#",
                    "#...######.........#",
                    "#..........M.......#",
                    "#..................#",
                    "#................E.#",
                    "####################"
                ]
            },
            {
                "name": "maze_like",
                "difficulty": "hard",
                "level": [
                    "####################",
                    "#P...##...##...##..#",
                    "#.T..##.M.##...##..#",
                    "#....##...##...##..#",
                    "##D####...####D##..#",
                    "#.....M...T........#",
                    "#.#####...#########",
                    "#.K...#...#.......E#",
                    "#.....#...#.M......#",
                    "#.....#...#........#",
                    "#.....#...#.T......#",
                    "####################"
                ]
            },
            {
                "name": "large_room",
                "difficulty": "medium",
                "level": [
                    "####################",
                    "#P.................#",
                    "#.################.#",
                    "#.#..............#.#",
                    "#.#..T...M...T...#.#",
                    "#.#..............#.#",
                    "#.#...M.....M....#.#",
                    "#.#..............#.#",
                    "#.#.....T........#.#",
                    "#.################.#",
                    "#................E.#",
                    "####################"
                ]
            },
            {
                "name": "multi_path",
                "difficulty": "easy",
                "level": [
                    "####################",
                    "#P.......#.........#",
                    "#..T.....#....M....#",
                    "#........#.........#",
                    "#########.#########",
                    "#........#.........#",
                    "#...M....#....T....#",
                    "#........#.........#",
                    "#########.#########",
                    "#........#.........#",
                    "#........#.......E.#",
                    "####################"
                ]
            }
        ]
        
        for example in examples:
            filepath = os.path.join(self.examples_dir, f"{example['name']}.json")
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    json.dump(example, f, indent=2)
    
    def load_examples(self):
        examples = []
        for filename in os.listdir(self.examples_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.examples_dir, filename)
                with open(filepath, 'r') as f:
                    examples.append(json.load(f))
        return examples
    
    def save_generated_level(self, level_lines, metadata=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"level_{timestamp}.json"
        filepath = os.path.join(self.generated_dir, filename)
        
        data = {
            "level": level_lines,
            "generated_at": timestamp,
            "metadata": metadata or {}
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath
    
    def load_generated_levels(self, limit=None):
        levels = []
        files = sorted(os.listdir(self.generated_dir), reverse=True)
        
        for filename in files[:limit] if limit else files:
            if filename.endswith('.json'):
                filepath = os.path.join(self.generated_dir, filename)
                with open(filepath, 'r') as f:
                    levels.append(json.load(f))
        
        return levels
    
    def get_random_example(self):
        examples = self.load_examples()
        return random.choice(examples) if examples else None
    
    def export_dataset(self, output_file="dataset.json"):
        examples = self.load_examples()
        generated = self.load_generated_levels()
        
        dataset = {
            "examples": examples,
            "generated": generated,
            "total_count": len(examples) + len(generated)
        }
        
        filepath = os.path.join(self.data_dir, output_file)
        with open(filepath, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        print(f"Dataset exported to {filepath}")
        return filepath

