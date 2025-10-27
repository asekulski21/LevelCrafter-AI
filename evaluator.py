import numpy as np
from level_validator import LevelValidator
from config import EVALUATION_METRICS

class LevelEvaluator:
    def __init__(self):
        self.metrics = EVALUATION_METRICS
    
    def evaluate_single(self, level_lines):
        validator = LevelValidator(level_lines)
        results = validator.validate_all()
        
        metrics = {
            'playability_score': 1.0 if results['playability'] else 0.0,
            'connectivity_score': results['connectivity'],
            'difficulty_score': results['difficulty'],
            'treasure_density': results['treasure_density'],
            'monster_density': results['monster_density']
        }
        
        overall_score = (
            metrics['playability_score'] * 0.4 +
            metrics['connectivity_score'] * 0.3 +
            (1.0 - abs(metrics['difficulty_score'] - 0.5) * 2) * 0.15 +
            min(metrics['treasure_density'] * 20, 1.0) * 0.075 +
            min(metrics['monster_density'] * 20, 1.0) * 0.075
        )
        
        metrics['overall_score'] = overall_score
        metrics['playability_message'] = results['playability_message']
        
        return metrics
    
    def evaluate_batch(self, levels):
        all_metrics = []
        
        for level in levels:
            metrics = self.evaluate_single(level)
            all_metrics.append(metrics)
        
        return all_metrics
    
    def calculate_diversity(self, levels):
        if len(levels) < 2:
            return 0.0
        
        level_arrays = []
        for level in levels:
            level_str = ''.join(level)
            level_array = np.array([ord(c) for c in level_str])
            level_arrays.append(level_array)
        
        total_distance = 0
        count = 0
        
        for i in range(len(level_arrays)):
            for j in range(i+1, len(level_arrays)):
                distance = np.sum(level_arrays[i] != level_arrays[j]) / len(level_arrays[i])
                total_distance += distance
                count += 1
        
        avg_diversity = total_distance / count if count > 0 else 0.0
        
        return avg_diversity
    
    def aggregate_metrics(self, batch_metrics):
        if not batch_metrics:
            return {}
        
        aggregated = {}
        
        metric_keys = [k for k in batch_metrics[0].keys() if k != 'playability_message']
        
        for key in metric_keys:
            values = [m[key] for m in batch_metrics]
            aggregated[f'{key}_mean'] = np.mean(values)
            aggregated[f'{key}_std'] = np.std(values)
            aggregated[f'{key}_min'] = np.min(values)
            aggregated[f'{key}_max'] = np.max(values)
        
        return aggregated
    
    def print_evaluation(self, metrics):
        print("\n" + "="*60)
        print("LEVEL EVALUATION RESULTS")
        print("="*60)
        print(f"Overall Score: {metrics['overall_score']:.3f}")
        print(f"Playability: {'✓ PASS' if metrics['playability_score'] > 0 else '✗ FAIL'}")
        print(f"  - {metrics['playability_message']}")
        print(f"Connectivity: {metrics['connectivity_score']:.3f}")
        print(f"Difficulty: {metrics['difficulty_score']:.3f}")
        print(f"Treasure Density: {metrics['treasure_density']:.4f}")
        print(f"Monster Density: {metrics['monster_density']:.4f}")
        print("="*60 + "\n")
    
    def print_batch_evaluation(self, batch_metrics, diversity_score=None):
        aggregated = self.aggregate_metrics(batch_metrics)
        
        print("\n" + "="*60)
        print("BATCH EVALUATION RESULTS")
        print("="*60)
        print(f"Number of Levels: {len(batch_metrics)}")
        print(f"\nOverall Score:")
        print(f"  Mean: {aggregated['overall_score_mean']:.3f} ± {aggregated['overall_score_std']:.3f}")
        print(f"  Range: [{aggregated['overall_score_min']:.3f}, {aggregated['overall_score_max']:.3f}]")
        
        print(f"\nPlayability Rate: {aggregated['playability_score_mean']*100:.1f}%")
        
        print(f"\nConnectivity:")
        print(f"  Mean: {aggregated['connectivity_score_mean']:.3f} ± {aggregated['connectivity_score_std']:.3f}")
        
        print(f"\nDifficulty:")
        print(f"  Mean: {aggregated['difficulty_score_mean']:.3f} ± {aggregated['difficulty_score_std']:.3f}")
        
        if diversity_score is not None:
            print(f"\nDiversity Score: {diversity_score:.3f}")
        
        print("="*60 + "\n")

