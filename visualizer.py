import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from config import TILE_TYPES

class LevelVisualizer:
    def __init__(self):
        self.colors = {
            '#': (0.2, 0.2, 0.2),
            '.': (0.9, 0.9, 0.9),
            'P': (0.2, 0.8, 0.2),
            'E': (0.8, 0.2, 0.2),
            'T': (1.0, 0.84, 0.0),
            'M': (0.6, 0.2, 0.8),
            'K': (0.2, 0.6, 0.8),
            'D': (0.6, 0.4, 0.2),
            ' ': (0.0, 0.0, 0.0)
        }
        
        self.symbols = {
            'P': 'P',
            'E': 'E',
            'T': '$',
            'M': 'M',
            'K': 'K',
            'D': 'D'
        }
    
    def level_to_image(self, level_lines):
        height = len(level_lines)
        width = len(level_lines[0]) if height > 0 else 0
        
        img_array = np.zeros((height, width, 3))
        
        for i, line in enumerate(level_lines):
            for j, char in enumerate(line):
                color = self.colors.get(char, (0.5, 0.5, 0.5))
                img_array[i, j] = color
        
        return img_array
    
    def visualize(self, level_lines, title="Generated Level", save_path=None):
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        img_array = self.level_to_image(level_lines)
        ax.imshow(img_array, interpolation='nearest')
        
        for i, line in enumerate(level_lines):
            for j, char in enumerate(line):
                if char in self.symbols:
                    ax.text(j, i, self.symbols[char], 
                           ha='center', va='center',
                           fontsize=12, fontweight='bold',
                           color='white' if char in ['M', 'D'] else 'black')
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xticks(range(len(level_lines[0])))
        ax.set_yticks(range(len(level_lines)))
        ax.grid(True, alpha=0.3)
        
        legend_elements = [
            patches.Patch(facecolor=self.colors['#'], label='Wall'),
            patches.Patch(facecolor=self.colors['.'], label='Floor'),
            patches.Patch(facecolor=self.colors['P'], label='Player'),
            patches.Patch(facecolor=self.colors['E'], label='Exit'),
            patches.Patch(facecolor=self.colors['T'], label='Treasure'),
            patches.Patch(facecolor=self.colors['M'], label='Monster'),
            patches.Patch(facecolor=self.colors['K'], label='Key'),
            patches.Patch(facecolor=self.colors['D'], label='Door')
        ]
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Level visualization saved to {save_path}")
        
        plt.show()
    
    def visualize_multiple(self, levels, titles=None, save_path=None):
        n = len(levels)
        cols = min(3, n)
        rows = (n + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 4*rows))
        if n == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if n > 1 else [axes]
        
        for idx, level_lines in enumerate(levels):
            if idx >= len(axes):
                break
            
            ax = axes[idx]
            img_array = self.level_to_image(level_lines)
            ax.imshow(img_array, interpolation='nearest')
            
            for i, line in enumerate(level_lines):
                for j, char in enumerate(line):
                    if char in self.symbols:
                        ax.text(j, i, self.symbols[char], 
                               ha='center', va='center',
                               fontsize=8, fontweight='bold',
                               color='white' if char in ['M', 'D'] else 'black')
            
            title = titles[idx] if titles and idx < len(titles) else f"Level {idx+1}"
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
        
        for idx in range(len(levels), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Multiple levels visualization saved to {save_path}")
        
        plt.show()
    
    def print_ascii(self, level_lines):
        print("\n" + "="*50)
        for line in level_lines:
            print(line)
        print("="*50 + "\n")

