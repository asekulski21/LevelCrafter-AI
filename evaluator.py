# Level Evaluator - calculates quality metrics for levels

from validator import LevelValidator

class LevelEvaluator:
    """Evaluates the quality of generated levels."""
    
    def evaluate(self, level):
        """Calculate metrics for a single level."""
        validator = LevelValidator(level)
        
        playable, msg = validator.is_playable()
        connectivity = validator.get_connectivity()
        
        # Count elements
        level_str = ''.join(level)
        monsters = level_str.count('M')
        treasures = level_str.count('T')
        total_tiles = len(level_str)
        
        # Calculate scores
        metrics = {
            'playable': playable,
            'message': msg,
            'connectivity': round(connectivity, 3),
            'monsters': monsters,
            'treasures': treasures,
            'monster_density': round(monsters / total_tiles, 4),
            'treasure_density': round(treasures / total_tiles, 4)
        }
        
        # Overall score (0-1)
        score = 0.0
        if playable:
            score += 0.5
        score += connectivity * 0.3
        score += min(monsters * 0.02, 0.1)
        score += min(treasures * 0.02, 0.1)
        
        metrics['score'] = round(score, 3)
        
        return metrics
    
    def evaluate_batch(self, levels):
        """Evaluate multiple levels and calculate averages."""
        results = [self.evaluate(level) for level in levels]
        
        playable_count = sum(1 for r in results if r['playable'])
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_connectivity = sum(r['connectivity'] for r in results) / len(results)
        
        return {
            'count': len(levels),
            'playable_count': playable_count,
            'playability_rate': round(playable_count / len(levels) * 100, 1),
            'avg_score': round(avg_score, 3),
            'avg_connectivity': round(avg_connectivity, 3)
        }
    
    def print_results(self, metrics):
        """Print evaluation results."""
        print("\n" + "="*50)
        print("EVALUATION RESULTS")
        print("="*50)
        print(f"Playable: {'Yes' if metrics['playable'] else 'No'} - {metrics['message']}")
        print(f"Score: {metrics['score']}")
        print(f"Connectivity: {metrics['connectivity']}")
        print(f"Monsters: {metrics['monsters']}")
        print(f"Treasures: {metrics['treasures']}")
        print("="*50)
