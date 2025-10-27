from level_generator import LevelGenerator
from visualizer import LevelVisualizer
from evaluator import LevelEvaluator

def main():
    print("\n" + "="*60)
    print("QUICK DEMO: Procedural Level Generator")
    print("="*60)
    
    print("\nInitializing system (first run will download model ~2GB)...")
    generator = LevelGenerator()
    visualizer = LevelVisualizer()
    evaluator = LevelEvaluator()
    
    print("\nGenerating 3 levels with different difficulties...\n")
    
    difficulties = ["easy", "medium", "hard"]
    levels = []
    
    for difficulty in difficulties:
        print(f"\nGenerating {difficulty.upper()} level...")
        level = generator.generate(difficulty=difficulty, num_treasures=3, num_monsters=5)
        levels.append(level)
        
        print(f"\n--- {difficulty.upper()} LEVEL ---")
        visualizer.print_ascii(level)
        
        metrics = evaluator.evaluate_single(level)
        print(f"Playability: {'✓ PASS' if metrics['playability_score'] > 0 else '✗ FAIL'}")
        print(f"Overall Score: {metrics['overall_score']:.3f}")
        print(f"Difficulty: {metrics['difficulty_score']:.3f}")
    
    print("\n" + "="*60)
    print("Calculating batch metrics...")
    batch_metrics = evaluator.evaluate_batch(levels)
    diversity = evaluator.calculate_diversity(levels)
    
    evaluator.print_batch_evaluation(batch_metrics, diversity)
    
    print("\nDemo complete! Run 'python main.py interactive' for full features.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

