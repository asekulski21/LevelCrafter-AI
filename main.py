# LevelCrafter-AI
# Procedural Game Level Generator using Large Language Model
# CSI-4130/5130 Artificial Intelligence Course Project

from level_generator import LevelGenerator
from evaluator import LevelEvaluator

# Example levels
EXAMPLES = [
    {
        "name": "Simple Corridor",
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
        "name": "Room Layout",
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
    }
]


def print_level(level):
    """Print a level as ASCII."""
    print("=" * len(level[0]))
    for row in level:
        print(row)
    print("=" * len(level[0]))


def show_examples():
    """Display example levels."""
    evaluator = LevelEvaluator()
    
    print("\n" + "="*50)
    print("EXAMPLE LEVELS")
    print("="*50)
    
    for ex in EXAMPLES:
        print(f"\n{ex['name']}:")
        print_level(ex['level'])
        metrics = evaluator.evaluate(ex['level'])
        print(f"Playable: {'Yes' if metrics['playable'] else 'No'}")


def generate_levels():
    """Generate new levels using the LLM."""
    print("\n" + "="*50)
    print("GENERATING LEVELS WITH LLM")
    print("="*50)
    
    generator = LevelGenerator()
    evaluator = LevelEvaluator()
    
    levels = []
    for diff in ["easy", "medium", "hard"]:
        print(f"\nGenerating {diff} level...")
        level = generator.generate(difficulty=diff)
        levels.append(level)
        
        print_level(level)
        
        metrics = evaluator.evaluate(level)
        print(f"Playable: {'Yes' if metrics['playable'] else 'No'}")
        print(f"Score: {metrics['score']}")
        print(f"Connectivity: {metrics['connectivity']}")
    
    # Batch results
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    batch = evaluator.evaluate_batch(levels)
    print(f"Levels: {batch['count']}")
    print(f"Playable: {batch['playable_count']}/{batch['count']} ({batch['playability_rate']}%)")
    print(f"Average score: {batch['avg_score']}")
    
    return levels


def demo():
    """Run demo for presentation."""
    print("\n" + "="*50)
    print("LEVELCRAFTER-AI")
    print("Procedural Level Generator using LLM")
    print("="*50)
    
    input("\nPress Enter to see example levels...")
    show_examples()
    
    input("\nPress Enter to generate levels with AI...")
    generate_levels()
    
    print("\n" + "="*50)
    print("DEMO COMPLETE")
    print("="*50)
    print("\nSummary:")
    print("- Uses TinyLlama (1.1B parameter LLM)")
    print("- BFS algorithm validates playability")
    print("- Post-processing fixes AI errors")


def interactive():
    """Interactive mode."""
    generator = None
    evaluator = LevelEvaluator()
    
    while True:
        print("\n" + "="*40)
        print("LEVELCRAFTER-AI")
        print("="*40)
        print("1. Show examples")
        print("2. Generate a level")
        print("3. Generate multiple levels")
        print("4. Run demo")
        print("5. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            show_examples()
        
        elif choice == "2":
            if generator is None:
                print("\nLoading model...")
                generator = LevelGenerator()
            
            diff = input("Difficulty (easy/medium/hard) [medium]: ").strip() or "medium"
            print(f"\nGenerating {diff} level...")
            level = generator.generate(difficulty=diff)
            
            print_level(level)
            metrics = evaluator.evaluate(level)
            print(f"Playable: {'Yes' if metrics['playable'] else 'No'}")
            print(f"Score: {metrics['score']}")
        
        elif choice == "3":
            if generator is None:
                print("\nLoading model...")
                generator = LevelGenerator()
            
            count = input("How many? [3]: ").strip()
            count = int(count) if count.isdigit() else 3
            
            levels = []
            for i in range(count):
                print(f"\nGenerating level {i+1}/{count}...")
                level = generator.generate()
                levels.append(level)
                print_level(level)
            
            batch = evaluator.evaluate_batch(levels)
            print(f"\nPlayability: {batch['playability_rate']}%")
            print(f"Average score: {batch['avg_score']}")
        
        elif choice == "4":
            demo()
        
        elif choice == "5":
            print("Goodbye!")
            break


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        interactive()
