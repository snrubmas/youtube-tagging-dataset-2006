#!/usr/bin/env python3
"""
YouTube Tagging Dataset (2006-2007) - Statistics Generator
Generates comprehensive statistics and visualizations for the dataset landing page.

Usage:
    python generate_statistics.py --db youtube_2006.db --output-dir docs/assets/images/visualizations
"""

import sqlite3
import json
import argparse
from datetime import datetime
from collections import Counter
import statistics
from pathlib import Path


class YouTubeDatasetAnalyzer:
    """Analyzes the YouTube 2006-2007 tagging dataset and generates statistics."""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.stats = {}
        
    def get_basic_counts(self):
        """Get basic dataset counts."""
        cursor = self.conn.cursor()
        
        # Video count
        cursor.execute("SELECT COUNT(*) as count FROM videos")
        video_count = cursor.fetchone()['count']
        
        # Tag count
        cursor.execute("SELECT COUNT(*) as count FROM tags")
        tag_count = cursor.fetchone()['count']
        
        # Video-tag relationships
        cursor.execute("SELECT COUNT(*) as count FROM video_tag_key")
        relationship_count = cursor.fetchone()['count']
        
        # Unique authors
        cursor.execute("SELECT COUNT(DISTINCT author) as count FROM videos")
        author_count = cursor.fetchone()['count']
        
        self.stats['basic_counts'] = {
            'videos': video_count,
            'tags': tag_count,
            'video_tag_pairs': relationship_count,
            'unique_authors': author_count
        }
        
        print(f"✓ Basic counts: {video_count:,} videos, {tag_count:,} tags")
        
    def analyze_tags_per_video(self):
        """Analyze distribution of tags per video."""
        cursor = self.conn.cursor()
        
        query = """
        SELECT COUNT(tag_id) as tag_count
        FROM video_tag_key
        GROUP BY vid_id
        """
        
        cursor.execute(query)
        tag_counts = [row['tag_count'] for row in cursor.fetchall()]
        
        self.stats['tags_per_video'] = {
            'mean': round(statistics.mean(tag_counts), 2),
            'median': statistics.median(tag_counts),
            'mode': statistics.mode(tag_counts) if tag_counts else 0,
            'min': min(tag_counts),
            'max': max(tag_counts),
            'std_dev': round(statistics.stdev(tag_counts), 2),
            'distribution': dict(Counter(tag_counts).most_common(20))
        }
        
        print(f"✓ Tags per video: mean={self.stats['tags_per_video']['mean']}, "
              f"median={self.stats['tags_per_video']['median']}")
        
    def analyze_videos_per_author(self):
        """Analyze distribution of videos per author."""
        cursor = self.conn.cursor()
        
        query = """
        SELECT author, COUNT(*) as video_count
        FROM videos
        GROUP BY author
        """
        
        cursor.execute(query)
        video_counts = [row['video_count'] for row in cursor.fetchall()]
        
        self.stats['videos_per_author'] = {
            'mean': round(statistics.mean(video_counts), 2),
            'median': statistics.median(video_counts),
            'min': min(video_counts),
            'max': max(video_counts),
            'std_dev': round(statistics.stdev(video_counts), 2)
        }
        
        # Top uploaders
        cursor.execute("""
        SELECT author, COUNT(*) as video_count
        FROM videos
        GROUP BY author
        ORDER BY video_count DESC
        LIMIT 20
        """)
        
        self.stats['top_uploaders'] = [
            {'author': row['author'], 'videos': row['video_count']}
            for row in cursor.fetchall()
        ]
        
        print(f"✓ Videos per author: mean={self.stats['videos_per_author']['mean']}, "
              f"max={self.stats['videos_per_author']['max']}")
        
    def analyze_popular_tags(self):
        """Find most popular tags."""
        cursor = self.conn.cursor()
        
        query = """
        SELECT t.tag, COUNT(vtk.vid_id) as usage_count
        FROM tags t
        JOIN video_tag_key vtk ON t.tag_id = vtk.tag_id
        GROUP BY t.tag_id
        ORDER BY usage_count DESC
        LIMIT 50
        """
        
        cursor.execute(query)
        self.stats['top_tags'] = [
            {'tag': row['tag'], 'count': row['usage_count']}
            for row in cursor.fetchall()
        ]
        
        print(f"✓ Top tag: '{self.stats['top_tags'][0]['tag']}' "
              f"({self.stats['top_tags'][0]['count']:,} uses)")
        
    def analyze_video_lengths(self):
        """Analyze video length distribution."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT length_seconds
        FROM videos
        WHERE length_seconds IS NOT NULL AND length_seconds > 0
        """)
        
        lengths = [row['length_seconds'] for row in cursor.fetchall()]
        
        if lengths:
            self.stats['video_lengths'] = {
                'mean_seconds': round(statistics.mean(lengths), 2),
                'mean_minutes': round(statistics.mean(lengths) / 60, 2),
                'median_seconds': statistics.median(lengths),
                'median_minutes': round(statistics.median(lengths) / 60, 2),
                'min_seconds': min(lengths),
                'max_seconds': max(lengths),
                'max_minutes': round(max(lengths) / 60, 2)
            }
            
            print(f"✓ Video length: mean={self.stats['video_lengths']['mean_minutes']} min, "
                  f"median={self.stats['video_lengths']['median_minutes']} min")
        
    def analyze_view_counts(self):
        """Analyze view count statistics."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT view_count
        FROM videos
        WHERE view_count IS NOT NULL AND view_count > 0
        ORDER BY view_count DESC
        """)
        
        view_counts = [row['view_count'] for row in cursor.fetchall()]
        
        if view_counts:
            self.stats['view_counts'] = {
                'total_views': sum(view_counts),
                'mean': round(statistics.mean(view_counts), 2),
                'median': statistics.median(view_counts),
                'max': max(view_counts),
                'percentile_90': self._percentile(view_counts, 90),
                'percentile_95': self._percentile(view_counts, 95),
                'percentile_99': self._percentile(view_counts, 99)
            }
            
            print(f"✓ Total views: {self.stats['view_counts']['total_views']:,}")
        
    def analyze_ratings(self):
        """Analyze video ratings."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT rating_avg, rating_count
        FROM videos
        WHERE rating_avg IS NOT NULL AND rating_count > 0
        """)
        
        ratings = [(row['rating_avg'], row['rating_count']) for row in cursor.fetchall()]
        
        if ratings:
            avg_ratings = [r[0] for r in ratings]
            rating_counts = [r[1] for r in ratings]
            
            self.stats['ratings'] = {
                'videos_with_ratings': len(ratings),
                'mean_rating': round(statistics.mean(avg_ratings), 2),
                'median_rating': round(statistics.median(avg_ratings), 2),
                'mean_rating_count': round(statistics.mean(rating_counts), 2),
                'median_rating_count': statistics.median(rating_counts)
            }
            
            print(f"✓ Ratings: mean={self.stats['ratings']['mean_rating']}/5.0")
        
    def analyze_temporal_distribution(self):
        """Analyze upload time distribution."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT upload_time
        FROM videos
        WHERE upload_time IS NOT NULL
        ORDER BY upload_time
        """)
        
        timestamps = [row['upload_time'] for row in cursor.fetchall()]
        
        if timestamps:
            # Convert to datetime for analysis
            dates = [datetime.fromtimestamp(ts) for ts in timestamps if ts > 0]
            
            if dates:
                self.stats['temporal'] = {
                    'earliest_upload': dates[0].strftime('%Y-%m-%d'),
                    'latest_upload': dates[-1].strftime('%Y-%m-%d'),
                    'collection_days': (dates[-1] - dates[0]).days
                }
                
                # Uploads by month
                month_counts = Counter(d.strftime('%Y-%m') for d in dates)
                self.stats['temporal']['uploads_by_month'] = dict(
                    sorted(month_counts.items())
                )
                
                print(f"✓ Collection period: {self.stats['temporal']['earliest_upload']} "
                      f"to {self.stats['temporal']['latest_upload']}")
        
    def analyze_tag_characteristics(self):
        """Analyze tag text characteristics."""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT tag FROM tags")
        tags = [row['tag'] for row in cursor.fetchall()]
        
        # Tag length statistics
        tag_lengths = [len(tag) for tag in tags]
        
        # Multi-word tags
        multi_word = sum(1 for tag in tags if ' ' in tag)
        
        # Tags with special characters
        special_chars = sum(1 for tag in tags if any(c in tag for c in '!@#$%^&*()'))
        
        self.stats['tag_characteristics'] = {
            'mean_length': round(statistics.mean(tag_lengths), 2),
            'median_length': statistics.median(tag_lengths),
            'min_length': min(tag_lengths),
            'max_length': max(tag_lengths),
            'multi_word_count': multi_word,
            'multi_word_percent': round(multi_word / len(tags) * 100, 2),
            'with_special_chars': special_chars
        }
        
        print(f"✓ Tag characteristics: {multi_word:,} multi-word tags "
              f"({self.stats['tag_characteristics']['multi_word_percent']}%)")
        
    def analyze_tag_cooccurrence(self):
        """Find most common tag pairs."""
        cursor = self.conn.cursor()
        
        # Get tag pairs that appear together
        query = """
        SELECT t1.tag as tag1, t2.tag as tag2, COUNT(*) as cooccurrence
        FROM video_tag_key vtk1
        JOIN video_tag_key vtk2 ON vtk1.vid_id = vtk2.vid_id
        JOIN tags t1 ON vtk1.tag_id = t1.tag_id
        JOIN tags t2 ON vtk2.tag_id = t2.tag_id
        WHERE vtk1.tag_id < vtk2.tag_id
        GROUP BY vtk1.tag_id, vtk2.tag_id
        ORDER BY cooccurrence DESC
        LIMIT 30
        """
        
        cursor.execute(query)
        self.stats['tag_cooccurrence'] = [
            {
                'tag1': row['tag1'],
                'tag2': row['tag2'],
                'count': row['cooccurrence']
            }
            for row in cursor.fetchall()
        ]
        
        print(f"✓ Tag co-occurrence analyzed (top 30 pairs)")
        
    def _percentile(self, data, percent):
        """Calculate percentile of sorted data."""
        k = (len(data) - 1) * percent / 100
        f = int(k)
        c = k - f
        if f + 1 < len(data):
            return data[f] + c * (data[f + 1] - data[f])
        return data[f]
    
    def generate_summary_text(self):
        """Generate human-readable summary."""
        summary = {
            'title': 'YouTube Tagging Dataset (2006-2007)',
            'subtitle': 'A Historical Snapshot of Early YouTube Community Practices',
            'highlights': [
                f"{self.stats['basic_counts']['videos']:,} unique videos",
                f"{self.stats['basic_counts']['tags']:,} unique tags",
                f"{self.stats['basic_counts']['video_tag_pairs']:,} video-tag relationships",
                f"{self.stats['basic_counts']['unique_authors']:,} content creators",
                f"Collected over {self.stats['temporal']['collection_days']} days",
                f"Average {self.stats['tags_per_video']['mean']} tags per video"
            ],
            'key_findings': [
                f"Most popular tag: '{self.stats['top_tags'][0]['tag']}' ({self.stats['top_tags'][0]['count']:,} uses)",
                f"Most prolific uploader: {self.stats['top_uploaders'][0]['videos']:,} videos",
                f"{self.stats['tag_characteristics']['multi_word_percent']}% of tags contain multiple words",
                f"Total accumulated views: {self.stats['view_counts']['total_views']:,}"
            ]
        }
        
        self.stats['summary'] = summary
        
    def run_all_analyses(self):
        """Run all analysis methods."""
        print("Analyzing YouTube Tagging Dataset (2006-2007)")
        print("=" * 60)
        
        self.get_basic_counts()
        self.analyze_tags_per_video()
        self.analyze_videos_per_author()
        self.analyze_popular_tags()
        self.analyze_video_lengths()
        self.analyze_view_counts()
        self.analyze_ratings()
        self.analyze_temporal_distribution()
        self.analyze_tag_characteristics()
        self.analyze_tag_cooccurrence()
        self.generate_summary_text()
        
        print("=" * 60)
        print("✓ All analyses complete!")
        
    def save_statistics(self, output_path):
        """Save statistics to JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Statistics saved to: {output_file}")
        
    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='Generate statistics for YouTube Tagging Dataset (2006-2007)'
    )
    parser.add_argument(
        '--db',
        required=True,
        help='Path to SQLite database file'
    )
    parser.add_argument(
        '--output',
        default='analysis/summary_statistics.json',
        help='Output JSON file path'
    )
    
    args = parser.parse_args()
    
    # Run analysis
    analyzer = YouTubeDatasetAnalyzer(args.db)
    analyzer.run_all_analyses()
    analyzer.save_statistics(args.output)
    analyzer.close()
    
    print("\nNext steps:")
    print("1. Review the generated statistics in the output JSON")
    print("2. Run create_visualizations.py to generate charts")
    print("3. Use the stats to populate your landing page")


if __name__ == '__main__':
    main()
