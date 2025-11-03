#!/usr/bin/env python3
"""
YouTube Tagging Dataset - Visualization Generator
Creates charts and visualizations for the landing page.

Usage:
    python create_visualizations.py --stats analysis/summary_statistics.json --output-dir docs/assets/images/visualizations
"""

import json
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import numpy as np
from datetime import datetime


class DatasetVisualizer:
    """Creates visualizations for the YouTube dataset."""
    
    def __init__(self, stats_path, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(stats_path, 'r') as f:
            self.stats = json.load(f)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = ['#FF0000', '#282828', '#065FD4', '#AAAAAA', '#666666']
        
    def create_tags_per_video_distribution(self):
        """Create histogram of tags per video."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        distribution = self.stats['tags_per_video']['distribution']
        x = sorted([int(k) for k in distribution.keys()])
        y = [distribution[str(k)] for k in x]
        
        # Limit to reasonable range for visualization
        max_x = 30
        x_limited = [i for i in x if i <= max_x]
        y_limited = [y[i] for i in range(len(x)) if x[i] <= max_x]
        
        ax.bar(x_limited, y_limited, color=self.colors[0], alpha=0.7, edgecolor='black')
        ax.set_xlabel('Number of Tags', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Videos', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Tags per Video', fontsize=14, fontweight='bold', pad=20)
        
        # Add mean and median lines
        mean = self.stats['tags_per_video']['mean']
        median = self.stats['tags_per_video']['median']
        ax.axvline(mean, color='green', linestyle='--', linewidth=2, label=f'Mean: {mean}')
        ax.axvline(median, color='orange', linestyle='--', linewidth=2, label=f'Median: {median}')
        ax.legend()
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'tags_per_video.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✓ Created: tags_per_video.png")
        
    def create_top_tags_chart(self):
        """Create horizontal bar chart of top tags."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        top_tags = self.stats['top_tags'][:20]
        tags = [item['tag'] for item in top_tags]
        counts = [item['count'] for item in top_tags]
        
        y_pos = np.arange(len(tags))
        ax.barh(y_pos, counts, color=self.colors[2], edgecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(tags)
        ax.invert_yaxis()
        ax.set_xlabel('Number of Uses', fontsize=12, fontweight='bold')
        ax.set_title('Top 20 Most Popular Tags', fontsize=14, fontweight='bold', pad=20)
        
        # Add value labels
        for i, v in enumerate(counts):
            ax.text(v, i, f' {v:,}', va='center', fontweight='bold')
        
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_tags.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✓ Created: top_tags.png")
        
    def create_uploaders_distribution(self):
        """Create visualization of uploader activity."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        top_uploaders = self.stats['top_uploaders'][:15]
        authors = [f"User {i+1}" for i in range(len(top_uploaders))]  # Anonymize
        videos = [item['videos'] for item in top_uploaders]
        
        x_pos = np.arange(len(authors))
        ax.bar(x_pos, videos, color=self.colors[0], alpha=0.7, edgecolor='black')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(authors, rotation=45, ha='right')
        ax.set_ylabel('Number of Videos', fontsize=12, fontweight='bold')
        ax.set_title('Top 15 Most Prolific Uploaders', fontsize=14, fontweight='bold', pad=20)
        
        # Add value labels
        for i, v in enumerate(videos):
            ax.text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold')
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_uploaders.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✓ Created: top_uploaders.png")
        
    def create_temporal_timeline(self):
        """Create timeline of uploads over collection period."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        uploads_by_month = self.stats['temporal']['uploads_by_month']
        months = list(uploads_by_month.keys())
        counts = list(uploads_by_month.values())
        
        x_pos = np.arange(len(months))
        ax.plot(x_pos, counts, marker='o', linewidth=2, markersize=8, 
                color=self.colors[2])
        ax.fill_between(x_pos, counts, alpha=0.3, color=self.colors[2])
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(months, rotation=45, ha='right')
        ax.set_ylabel('Number of Uploads', fontsize=12, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_title('Upload Activity Over Collection Period', 
                     fontsize=14, fontweight='bold', pad=20)
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'temporal_timeline.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✓ Created: temporal_timeline.png")
        
    def create_overview_infographic(self):
        """Create summary infographic with key statistics."""
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_facecolor('white')
        
        # Remove axes
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.95, 'YouTube Tagging Dataset (2006-2007)', 
                ha='center', va='top', fontsize=24, fontweight='bold',
                transform=ax.transAxes)
        
        ax.text(0.5, 0.90, 'A Historical Snapshot of Early YouTube', 
                ha='center', va='top', fontsize=14, style='italic',
                transform=ax.transAxes, color='#666666')
        
        # Key statistics in boxes
        stats_data = [
            ('Videos', f"{self.stats['basic_counts']['videos']:,}"),
            ('Unique Tags', f"{self.stats['basic_counts']['tags']:,}"),
            ('Video-Tag Pairs', f"{self.stats['basic_counts']['video_tag_pairs']:,}"),
            ('Content Creators', f"{self.stats['basic_counts']['unique_authors']:,}"),
            ('Collection Period', f"{self.stats['temporal']['collection_days']} days"),
            ('Avg Tags/Video', f"{self.stats['tags_per_video']['mean']}")
        ]
        
        # Create grid of boxes
        box_positions = [
            (0.17, 0.65), (0.50, 0.65), (0.83, 0.65),
            (0.17, 0.40), (0.50, 0.40), (0.83, 0.40)
        ]
        
        for (x, y), (label, value) in zip(box_positions, stats_data):
            # Draw box
            box = plt.Rectangle((x-0.12, y-0.08), 0.24, 0.16, 
                               transform=ax.transAxes,
                               facecolor='#f0f0f0', edgecolor='#333333', 
                               linewidth=2)
            ax.add_patch(box)
            
            # Add text
            ax.text(x, y+0.04, value, ha='center', va='center',
                   fontsize=18, fontweight='bold', transform=ax.transAxes,
                   color=self.colors[0])
            ax.text(x, y-0.04, label, ha='center', va='center',
                   fontsize=10, transform=ax.transAxes, color='#666666')
        
        # Bottom section with highlights
        highlights = [
            f"• Most popular tag: '{self.stats['top_tags'][0]['tag']}' ({self.stats['top_tags'][0]['count']:,} uses)",
            f"• {self.stats['tag_characteristics']['multi_word_percent']}% of tags contain multiple words",
            f"• Average video length: {self.stats['video_lengths']['mean_minutes']} minutes",
            f"• Total accumulated views: {self.stats['view_counts']['total_views']:,}"
        ]
        
        y_pos = 0.20
        for highlight in highlights:
            ax.text(0.5, y_pos, highlight, ha='center', va='top',
                   fontsize=11, transform=ax.transAxes)
            y_pos -= 0.04
        
        # Footer
        ax.text(0.5, 0.02, 'Burns, S. & Geisler, G. (2006-2007) | DOI: 10.5281/zenodo.17508119', 
                ha='center', va='bottom', fontsize=9, style='italic',
                transform=ax.transAxes, color='#999999')
        
        plt.savefig(self.output_dir / 'overview_infographic.png', 
                   dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print("✓ Created: overview_infographic.png")
        
    def create_tag_cooccurrence_network(self):
        """Create visualization of top tag co-occurrences."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        cooccur = self.stats['tag_cooccurrence'][:10]
        
        # Create text representation
        ax.axis('off')
        ax.text(0.5, 0.95, 'Top Tag Co-occurrences', 
                ha='center', va='top', fontsize=16, fontweight='bold',
                transform=ax.transAxes)
        
        y_pos = 0.85
        for i, item in enumerate(cooccur, 1):
            text = f"{i}. '{item['tag1']}' + '{item['tag2']}' ({item['count']:,} videos)"
            ax.text(0.1, y_pos, text, ha='left', va='top',
                   fontsize=11, transform=ax.transAxes)
            y_pos -= 0.08
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'tag_cooccurrence.png', 
                   dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✓ Created: tag_cooccurrence.png")
        
    def create_all_visualizations(self):
        """Generate all visualizations."""
        print("Generating visualizations...")
        print("=" * 60)
        
        self.create_overview_infographic()
        self.create_tags_per_video_distribution()
        self.create_top_tags_chart()
        self.create_uploaders_distribution()
        self.create_temporal_timeline()
        self.create_tag_cooccurrence_network()
        
        print("=" * 60)
        print(f"✓ All visualizations saved to: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate visualizations for YouTube Tagging Dataset'
    )
    parser.add_argument(
        '--stats',
        required=True,
        help='Path to summary_statistics.json file'
    )
    parser.add_argument(
        '--output-dir',
        default='docs/assets/images/visualizations',
        help='Output directory for visualizations'
    )
    
    args = parser.parse_args()
    
    visualizer = DatasetVisualizer(args.stats, args.output_dir)
    visualizer.create_all_visualizations()
    
    print("\nNext step:")
    print("Create your landing page HTML using these visualizations!")


if __name__ == '__main__':
    main()
