import sys
from level_generator import LevelGenerator
from level_validator import LevelValidator
from evaluator import LevelEvaluator
from visualizer import LevelVisualizer
from dataset_manager import DatasetManager

def test_basic_functionality():
    print("="*60)
    print("TESTING PROCEDURAL LEVEL GENERATOR SYSTEM")
    print("="*60)
    
    print("\n[1/6] Testing Dataset Manager...")
    try:
        dm = DatasetManager()
        examples = dm.load_examples()
        print(f"✓ Dataset Manager working - {len(examples)} examples loaded")
    except Exception as e:
        print(f"✗ Dataset Manager failed: {e}")
        return False
    
    print("\n[2/6] Testing Level Validator...")
    try:
        if examples:
            validator = LevelValidator(examples[0]['level'])
            results = validator.validate_all()
            print(f"✓ Level Validator working - Playability: {results['playability']}")
        else:
            print("⚠ No examples to validate")
    except Exception as e:
        print(f"✗ Level Validator failed: {e}")
        return False
    
    print("\n[3/6] Testing Evaluator...")
    try:
        evaluator = LevelEvaluator()
        if examples:
            metrics = evaluator.evaluate_single(examples[0]['level'])
            print(f"✓ Evaluator working - Overall Score: {metrics['overall_score']:.3f}")
        else:
            print("⚠ No examples to evaluate")
    except Exception as e:
        print(f"✗ Evaluator failed: {e}")
        return False
    
    print("\n[4/6] Testing Visualizer...")
    try:
        visualizer = LevelVisualizer()
        if examples:
            visualizer.print_ascii(examples[0]['level'])
            print("✓ Visualizer working")
        else:
            print("⚠ No examples to visualize")
    except Exception as e:
        print(f"✗ Visualizer failed: {e}")
        return False
    
    print("\n[5/6] Testing LLM Engine (this will download the model)...")
    try:
        print("   This may take a few minutes on first run...")
        generator = LevelGenerator()
        print("✓ LLM Engine loaded successfully")
    except Exception as e:
        print(f"✗ LLM Engine failed: {e}")
        print("   Note: This requires significant RAM and downloads ~2GB model")
        return False
    
    print("\n[6/6] Testing Level Generation...")
    try:
        print("   Generating test level...")
        level = generator.generate(difficulty="easy", num_treasures=2, num_monsters=2)
        print("✓ Level Generation working")
        visualizer.print_ascii(level)
        
        metrics = evaluator.evaluate_single(level)
        evaluator.print_evaluation(metrics)
        
    except Exception as e:
        print(f"✗ Level Generation failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60)
    print("\nSystem is ready to use. Run 'python main.py interactive' to start.")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)

