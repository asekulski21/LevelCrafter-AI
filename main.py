import argparse
import sys
from level_generator import LevelGenerator
from visualizer import LevelVisualizer
from evaluator import LevelEvaluator
from dataset_manager import DatasetManager

def generate_single_level(args):
    print("Initializing Level Generator...")
    generator = LevelGenerator()
    visualizer = LevelVisualizer()
    evaluator = LevelEvaluator()
    
    print(f"Generating {args.difficulty} difficulty level...")
    level = generator.generate(
        difficulty=args.difficulty,
        num_treasures=args.treasures,
        num_monsters=args.monsters
    )
    
    visualizer.print_ascii(level)
    
    metrics = evaluator.evaluate_single(level)
    evaluator.print_evaluation(metrics)
    
    if args.visualize:
        visualizer.visualize(level, title=f"{args.difficulty.capitalize()} Difficulty Level")
    
    if args.save:
        dataset_manager = DatasetManager()
        filepath = dataset_manager.save_generated_level(level, {
            'difficulty': args.difficulty,
            'treasures': args.treasures,
            'monsters': args.monsters,
            'metrics': metrics
        })
        print(f"Level saved to {filepath}")

def generate_batch(args):
    print("Initializing Level Generator...")
    generator = LevelGenerator()
    visualizer = LevelVisualizer()
    evaluator = LevelEvaluator()
    dataset_manager = DatasetManager()
    
    print(f"Generating {args.count} levels...")
    levels = generator.generate_multiple(
        count=args.count,
        difficulty=args.difficulty
    )
    
    print("Evaluating generated levels...")
    batch_metrics = evaluator.evaluate_batch(levels)
    diversity_score = evaluator.calculate_diversity(levels)
    
    evaluator.print_batch_evaluation(batch_metrics, diversity_score)
    
    if args.visualize:
        visualizer.visualize_multiple(
            levels,
            titles=[f"Level {i+1} (Score: {batch_metrics[i]['overall_score']:.2f})" 
                   for i in range(len(levels))]
        )
    
    if args.save:
        for i, level in enumerate(levels):
            dataset_manager.save_generated_level(level, {
                'difficulty': args.difficulty,
                'batch_index': i,
                'metrics': batch_metrics[i]
            })
        print(f"Saved {len(levels)} levels")

def show_examples(args):
    dataset_manager = DatasetManager()
    visualizer = LevelVisualizer()
    
    examples = dataset_manager.load_examples()
    
    if not examples:
        print("No example levels found")
        return
    
    print(f"Found {len(examples)} example levels")
    
    for example in examples:
        print(f"\nExample: {example['name']} (Difficulty: {example['difficulty']})")
        visualizer.print_ascii(example['level'])
    
    if args.visualize:
        visualizer.visualize_multiple(
            [ex['level'] for ex in examples],
            titles=[f"{ex['name']} ({ex['difficulty']})" for ex in examples]
        )

def evaluate_dataset(args):
    dataset_manager = DatasetManager()
    evaluator = LevelEvaluator()
    
    if args.source == 'examples':
        examples = dataset_manager.load_examples()
        levels = [ex['level'] for ex in examples]
        print(f"Evaluating {len(levels)} example levels...")
    else:
        generated = dataset_manager.load_generated_levels(limit=args.limit)
        levels = [gen['level'] for gen in generated]
        print(f"Evaluating {len(levels)} generated levels...")
    
    if not levels:
        print("No levels found to evaluate")
        return
    
    batch_metrics = evaluator.evaluate_batch(levels)
    diversity_score = evaluator.calculate_diversity(levels)
    
    evaluator.print_batch_evaluation(batch_metrics, diversity_score)

def interactive_mode():
    print("\n" + "="*60)
    print("PROCEDURAL GAME LEVEL GENERATOR")
    print("="*60)
    print("\nWelcome to the Interactive Level Generator!")
    print("\nThis tool uses an open-source LLM (TinyLlama) to generate")
    print("playable dungeon levels procedurally.\n")
    
    generator = LevelGenerator()
    visualizer = LevelVisualizer()
    evaluator = LevelEvaluator()
    dataset_manager = DatasetManager()
    
    while True:
        print("\nOptions:")
        print("1. Generate a single level")
        print("2. Generate multiple levels")
        print("3. View example levels")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            difficulty = input("Enter difficulty (easy/medium/hard) [medium]: ").strip() or "medium"
            treasures = input("Number of treasures [3]: ").strip()
            treasures = int(treasures) if treasures.isdigit() else 3
            monsters = input("Number of monsters [5]: ").strip()
            monsters = int(monsters) if monsters.isdigit() else 5
            
            print("\nGenerating level...")
            level = generator.generate(difficulty, treasures, monsters)
            
            visualizer.print_ascii(level)
            metrics = evaluator.evaluate_single(level)
            evaluator.print_evaluation(metrics)
            
            if input("\nVisualize? (y/n): ").strip().lower() == 'y':
                visualizer.visualize(level)
            
            if input("Save level? (y/n): ").strip().lower() == 'y':
                filepath = dataset_manager.save_generated_level(level, {
                    'difficulty': difficulty,
                    'treasures': treasures,
                    'monsters': monsters,
                    'metrics': metrics
                })
                print(f"Saved to {filepath}")
        
        elif choice == '2':
            count = input("How many levels? [5]: ").strip()
            count = int(count) if count.isdigit() else 5
            difficulty = input("Enter difficulty (easy/medium/hard) [medium]: ").strip() or "medium"
            
            print(f"\nGenerating {count} levels...")
            levels = generator.generate_multiple(count, difficulty)
            
            print("Evaluating levels...")
            batch_metrics = evaluator.evaluate_batch(levels)
            diversity_score = evaluator.calculate_diversity(levels)
            
            evaluator.print_batch_evaluation(batch_metrics, diversity_score)
            
            if input("\nVisualize all? (y/n): ").strip().lower() == 'y':
                visualizer.visualize_multiple(levels)
        
        elif choice == '3':
            examples = dataset_manager.load_examples()
            print(f"\nFound {len(examples)} example levels:")
            for ex in examples:
                print(f"\n{ex['name']} ({ex['difficulty']})")
                visualizer.print_ascii(ex['level'])
        
        elif choice == '4':
            print("\nThank you for using the Level Generator!")
            break
        
        else:
            print("\nInvalid choice, please try again.")

def main():
    parser = argparse.ArgumentParser(
        description="Procedural Game Level Generator using LLM"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    generate_parser = subparsers.add_parser('generate', help='Generate a single level')
    generate_parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'],
                                 default='medium', help='Level difficulty')
    generate_parser.add_argument('--treasures', type=int, default=3,
                                 help='Number of treasures')
    generate_parser.add_argument('--monsters', type=int, default=5,
                                 help='Number of monsters')
    generate_parser.add_argument('--visualize', action='store_true',
                                 help='Visualize the generated level')
    generate_parser.add_argument('--save', action='store_true',
                                 help='Save the generated level')
    
    batch_parser = subparsers.add_parser('batch', help='Generate multiple levels')
    batch_parser.add_argument('--count', type=int, default=5,
                             help='Number of levels to generate')
    batch_parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'],
                             default='medium', help='Level difficulty')
    batch_parser.add_argument('--visualize', action='store_true',
                             help='Visualize all generated levels')
    batch_parser.add_argument('--save', action='store_true',
                             help='Save all generated levels')
    
    examples_parser = subparsers.add_parser('examples', help='Show example levels')
    examples_parser.add_argument('--visualize', action='store_true',
                                 help='Visualize example levels')
    
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate levels')
    eval_parser.add_argument('--source', choices=['examples', 'generated'],
                            default='generated', help='Source of levels to evaluate')
    eval_parser.add_argument('--limit', type=int, help='Limit number of levels')
    
    subparsers.add_parser('interactive', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        generate_single_level(args)
    elif args.command == 'batch':
        generate_batch(args)
    elif args.command == 'examples':
        show_examples(args)
    elif args.command == 'evaluate':
        evaluate_dataset(args)
    elif args.command == 'interactive':
        interactive_mode()
    else:
        interactive_mode()

if __name__ == "__main__":
    main()

