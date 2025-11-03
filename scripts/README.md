# YouTube Tagging Dataset - Scripts and Landing Page

This directory contains scripts to generate statistics, visualizations, and a static landing page for the YouTube Tagging Dataset (2006-2007).

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Statistics

```bash
python generate_statistics.py --db /path/to/youtube_2006.db --output analysis/summary_statistics.json
```

This will analyze the database and create a JSON file with comprehensive statistics.

### 3. Generate Visualizations

```bash
python create_visualizations.py --stats analysis/summary_statistics.json --output-dir docs/assets/images/visualizations
```

This creates PNG charts and graphs for the landing page.

### 4. Set Up Landing Page

```bash
# Create directory structure
mkdir -p docs/assets/css
mkdir -p docs/assets/js
mkdir -p docs/assets/images/visualizations

# Copy files
cp index.html docs/
cp style.css docs/assets/css/
cp main.js docs/assets/js/

# Your visualizations are already in docs/assets/images/visualizations/
```

### 5. Serve Locally (Optional)

```bash
cd docs
python -m http.server 8000
# Visit http://localhost:8000
```

## Script Details

### generate_statistics.py

Analyzes the SQLite database and generates comprehensive statistics including:
- Basic counts (videos, tags, authors, relationships)
- Tag distribution metrics
- Video length statistics
- View count analysis
- Temporal distribution
- Tag characteristics
- Co-occurrence patterns

**Usage:**
```bash
python generate_statistics.py --db youtube_2006.db --output analysis/summary_statistics.json
```

**Output:** JSON file with all statistics

### create_visualizations.py

Creates publication-quality visualizations from the statistics:
- Tags per video distribution
- Top 20 most popular tags
- Top uploaders (anonymized)
- Temporal timeline
- Tag co-occurrence
- Overview infographic

**Usage:**
```bash
python create_visualizations.py \
    --stats analysis/summary_statistics.json \
    --output-dir docs/assets/images/visualizations
```

**Output:** PNG files in the specified directory

## Landing Page

The landing page (`index.html`) is a modern, responsive single-page website featuring:

- **Hero section** with dataset overview
- **Statistics cards** with animated numbers
- **Key findings** in card layout
- **Visualizations** with generated charts
- **Research context** and publications
- **Use cases** for different research domains
- **Download options** for all data formats
- **Citation** with one-click copy

### Customization

1. **Update URLs**: Replace `snrubmas` in `index.html` with your GitHub username
2. **Add analytics**: Insert tracking code in `main.js`
3. **Modify colors**: Edit CSS variables in `style.css`:
   ```css
   :root {
       --color-primary: #FF0000;
       --color-secondary: #282828;
       --color-accent: #065FD4;
   }
   ```

### GitHub Pages Deployment

1. Push your repository to GitHub
2. Go to Settings → Pages
3. Select "Deploy from a branch"
4. Choose `main` branch and `/docs` folder
5. Save and wait for deployment

Your site will be available at: `https://snrubmas.github.io/youtube-tagging-dataset-2006/`

## File Structure

```
youtube-tagging-dataset-2006/
├── scripts/
│   ├── generate_statistics.py
│   ├── create_visualizations.py
│   └── requirements.txt
├── docs/
│   ├── index.html
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   │       └── visualizations/
│   │           ├── overview_infographic.png
│   │           ├── tags_per_video.png
│   │           ├── top_tags.png
│   │           ├── top_uploaders.png
│   │           ├── temporal_timeline.png
│   │           └── tag_cooccurrence.png
└── analysis/
    └── summary_statistics.json
```

## Additional Analysis

For more detailed analysis, consider:

1. **Jupyter Notebooks**: Create interactive analyses
   ```python
   import sqlite3
   import pandas as pd
   
   conn = sqlite3.connect('youtube_2006.db')
   df = pd.read_sql_query("SELECT * FROM videos LIMIT 1000", conn)
   ```

2. **Custom Queries**: Modify scripts for specific research questions

3. **Time Series Analysis**: Explore upload patterns over time

4. **Network Analysis**: Study tag co-occurrence networks

## Troubleshooting

### Database Path Issues
Make sure the SQLite database path is correct:
```bash
# Check if file exists
ls -lh youtube_2006.db

# Test database
sqlite3 youtube_2006.db "SELECT COUNT(*) FROM videos;"
```

### Matplotlib Backend Issues
If you get display errors, ensure you're using the 'Agg' backend:
```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
```

### Missing Dependencies
Install all required packages:
```bash
pip install matplotlib numpy pandas jupyter seaborn
```

## Contributing

If you create additional analysis scripts or visualizations, please consider contributing them back to the repository!

## License

Scripts are released under MIT License. The dataset itself is CC BY 4.0.

## Contact

For questions about these scripts:
- Open an issue on GitHub
- Contact: sburns@ischool.utexas.edu

## Citation

If you use these scripts in your research:

```bibtex
@misc{burns2025youtube_scripts,
  author = {Burns, Samuel A.},
  title = {Analysis Scripts for YouTube Tagging Dataset (2006-2007)},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/snrubmas/youtube-tagging-dataset-2006}
}
```
