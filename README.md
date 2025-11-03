# YouTube Tagging Dataset (2006-2007)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17508119.svg)](https://doi.org/10.5281/zenodo.17508119)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://snrubmas.github.io/youtube-tagging-dataset-2006/)

A historical collection of **1,092,310 YouTube videos** with user-generated tags, collected between November 2, 2006 and January 28, 2007. This dataset captures organic folksonomy and tagging practices from YouTube's first year of operation.

**📊 [View Interactive Landing Page](https://snrubmas.github.io/youtube-tagging-dataset-2006/)**

## 🎯 Quick Facts

- **Videos**: 1,092,310
- **Unique Tags**: 517,008  
- **Video-Tag Pairs**: 7,530,904
- **Content Creators**: 537,246
- **Collection Period**: 87 days (Nov 2, 2006 - Jan 28, 2007)
- **Average Tags/Video**: 6.9

## 📦 Download Dataset

The complete dataset is available on Zenodo:

**[Download from Zenodo](https://zenodo.org/records/17508119)** (DOI: 10.5281/zenodo.17508119)

### Available Formats

| Format | Size | Description | Use Case |
|--------|------|-------------|----------|
| **SQLite** | ~1.1 GB | Complete relational database | SQL queries, analysis |
| **CSV** | ~603 MB | Separate CSV files | Excel, R, Python pandas |
| **JSONL** | ~XXX MB | JSON Lines format | Streaming, web apps |
| **Samples** | ~1 MB | 1,000-record JSON samples | Testing, preview |

## 📁 Repository Structure

```
youtube-tagging-dataset-2006/
├── README.md                    # This file
├── DATA_DICTIONARY.md           # Field descriptions
├── LICENSE                      # CC BY 4.0
├── CITATION.cff                 # GitHub citation metadata
├── .gitignore                   # Git exclusions
│
├── docs/                        # GitHub Pages landing page
│   ├── index.html
│   ├── assets/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── images/visualizations/
│
├── data/
│   └── samples/                 # Small sample files
│       ├── videos_sample_1000.json
│       ├── tags_sample_1000.json
│       └── video_tag_key_sample_1000.json
│
├── scripts/                     # Analysis scripts
│   ├── generate_statistics.py
│   ├── create_visualizations.py
│   ├── requirements.txt
│   └── README.md
│
└── analysis/
    ├── summary_statistics.json
    └── example_queries.sql
```

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/snrubmas/youtube-tagging-dataset-2006.git
cd youtube-tagging-dataset-2006
```

### 2. Download Data

Download the database from [Zenodo](https://zenodo.org/records/17508119) and place it in the repository root:

```bash
# After downloading youtube_2006.db
mv ~/Downloads/youtube_2006.db .
```

### 3. Explore Sample Data

```python
import json

# Load sample videos
with open('data/samples/videos_sample_1000.json', 'r') as f:
    videos = json.load(f)
    
print(f"Loaded {len(videos)} sample videos")
print(f"First video: {videos[0]['title']}")
```

### 4. Query Database

```bash
sqlite3 youtube_2006.db

# Example queries
SELECT COUNT(*) FROM videos;
SELECT tag, COUNT(*) as usage FROM tags JOIN video_tag_key USING(tag_id) GROUP BY tag ORDER BY usage DESC LIMIT 10;
```

## 📊 Generate Statistics & Visualizations

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Generate statistics
python scripts/generate_statistics.py --db youtube_2006.db --output analysis/summary_statistics.json

# Create visualizations
python scripts/create_visualizations.py --stats analysis/summary_statistics.json --output-dir docs/assets/images/visualizations
```

See [scripts/README.md](scripts/README.md) for detailed documentation.

## 📚 Research Context

This dataset was collected as part of research on user-generated metadata and tagging conventions in video-sharing platforms. Key findings include:

- **Organic Folksonomy**: Captured before algorithmic recommendations, revealing natural tagging behaviors
- **Social Tagging**: ~66% of tags had zero algorithmic relevance to video metadata
- **Community Conventions**: Users developed collaborative practices for categorization and discovery

### Publications

1. **Geisler, G. and Burns, S.** (2007). "Tagging Video: Conventions and Strategies of the YouTube Community." *Proceedings of JCDL 2007*, p. 480. [DOI: 10.1145/1255175.1255279](https://doi.org/10.1145/1255175.1255279)

2. **Geisler, G. and Burns, S.** (2008). "Tagging Video: Conventions and Strategies of the YouTube Community." *IEEE TCDL Bulletin* 4(1).

## 🎓 Use Cases

This dataset is valuable for research in:

- **Information Science**: Folksonomy, collaborative tagging, metadata
- **Social Computing**: Early social media practices
- **Digital History**: YouTube's formative period
- **Computational Linguistics**: Natural language in tags
- **Information Retrieval**: Tag-based search algorithms
- **Cultural Studies**: 2006-2007 popular culture

## 📖 Documentation

- **[DATA_DICTIONARY.md](DATA_DICTIONARY.md)**: Complete field descriptions and schema
- **[Scripts README](scripts/README.md)**: Analysis scripts documentation  
- **[Landing Page](https://snrubmas.github.io/youtube-tagging-dataset-2006/)**: Interactive visualizations

## 🔍 Example Queries

### Most Popular Tags

```sql
SELECT t.tag, COUNT(vtk.vid_id) as usage_count
FROM tags t
JOIN video_tag_key vtk ON t.tag_id = vtk.tag_id
GROUP BY t.tag_id
ORDER BY usage_count DESC
LIMIT 20;
```

### Videos per User

```sql
SELECT author, COUNT(*) as video_count
FROM videos
GROUP BY author
ORDER BY video_count DESC
LIMIT 10;
```

### Tag Co-occurrence

```sql
SELECT t1.tag as tag1, t2.tag as tag2, COUNT(*) as cooccurrence
FROM video_tag_key vtk1
JOIN video_tag_key vtk2 ON vtk1.vid_id = vtk2.vid_id
JOIN tags t1 ON vtk1.tag_id = t1.tag_id
JOIN tags t2 ON vtk2.tag_id = t2.tag_id
WHERE vtk1.tag_id < vtk2.tag_id
GROUP BY vtk1.tag_id, vtk2.tag_id
ORDER BY cooccurrence DESC
LIMIT 20;
```

More examples in [analysis/example_queries.sql](analysis/example_queries.sql)

## ⚠️ Important Notes

### Historical Context

This data was collected during YouTube's first year when:
- The platform had different privacy norms
- Google's acquisition had just been announced
- Algorithmic recommendations were minimal
- Community-driven discovery was primary

### Known Limitations

1. **Incomplete Coverage**: Sample of YouTube, not comprehensive
2. **Deleted Content**: Many videos have been removed since 2006-2007
3. **API Constraints**: YouTube API v1 limitations
4. **Temporal Snapshot**: 3-month collection window

### Ethical Considerations

- Usernames are historical public data but consider anonymization for publications
- Content may have been deleted or made private by users since collection
- Follow your institution's IRB guidelines for historical social media data

## 📜 Citation

If you use this dataset, please cite:

```bibtex
@misc{burns2006youtube,
  author = {Burns, Samuel A. and Geisler, Gary},
  title = {YouTube Tagging Dataset (2006-2007)},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.17508119},
  url = {https://zenodo.org/records/17508119}
}
```

**And cite the associated research:**

```bibtex
@inproceedings{geisler2007tagging,
  author = {Geisler, Gary and Burns, Sam},
  title = {Tagging Video: Conventions and Strategies of the YouTube Community},
  booktitle = {Proceedings of the Joint Conference on Digital Libraries},
  year = {2007},
  pages = {480},
  doi = {10.1145/1255175.1255279}
}
```

## 📄 License

**Dataset**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

**Scripts**: MIT License

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Particularly interested in:
- Additional analysis scripts
- Visualizations
- Documentation improvements
- Bug fixes

## 📧 Contact

**Samuel A. Burns**  
School of Information  
The University of Texas at Austin  
📧 sburns@ischool.utexas.edu

For questions about:
- Dataset content → Open an issue
- Research collaboration → Email
- Technical problems → Open an issue

## 🙏 Acknowledgments

- **Gary Geisler**: Research collaboration and data collection
- **Dr. Randolph Bias**: Research advisor
- **The University of Texas at Austin**: School of Information support
- **IBM Pervasive Computing Lab**: Research context

---

⭐ **Star this repo** if you find it useful for your research!

📊 **[Explore the interactive landing page](https://snrubmas.github.io/youtube-tagging-dataset-2006/)**
