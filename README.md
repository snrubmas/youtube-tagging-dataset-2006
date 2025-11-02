# YouTube Tagging Dataset (2006-2007)

## Overview

This dataset contains tagging and metadata information from 1,092,310 YouTube videos collected between November 2, 2006 and January 28, 2007, representing one of the earliest systematic collections of YouTube user-generated metadata.

**Historical Context**: This data was collected during YouTube's first full year of operation, before the Google acquisition was finalized (October 2006) and before algorithmic recommendations became dominant. It captures organic folksonomy and tagging practices of YouTube's early community.

## Dataset Statistics

- **Collection Period**: November 2, 2006 - January 28, 2007
- **Unique Videos**: 1,092,310
- **Unique Tags**: 517,008
- **Total Video-Tag Pairs**: 7,530,904
- **Unique Users**: 537,246
- **Tags per Video**: Mean 6.9, Median 6, Range 1-60
- **Videos per User**: Mean 2.0, Median 1, Max 1,976

## Research Background

This dataset was collected as part of research on user-generated metadata and tagging conventions in video-sharing platforms. The research resulted in two publications:

1. **Geisler, G. and Burns, S.** (2008). "Tagging Video: Conventions and Strategies of the YouTube Community." *Bulletin of IEEE Technical Committee on Digital Libraries (TCDL)* 4(1). [poster report]

2. **Geisler, G. and Burns, S.** (2007). "Tagging Video: Conventions and Strategies of the YouTube Community." *Proceedings of the Joint Conference on Digital Libraries (JCDL 2007)*, p. 480. [poster]

## Data Collection Methodology

Data was collected using YouTube's early Data API (v1), which was publicly available at the time. The collection focused on:

- Video metadata (title, description, upload date, uploader)
- User-generated tags
- User information (username, upload count)
- Tag relevance to video metadata

### Collection Parameters

- API Version: YouTube Data API v1 (deprecated)
- Collection Method: Systematic sampling via API queries
- Time Period: 87 days (approximately 3 months)
- Geographic Scope: Global YouTube platform

## Data Structure

The dataset is provided in multiple formats:

### MySQL Database Files
- `mysql/` - Original MySQL database files (InnoDB/MyISAM)
- `mysql/schema.sql` - Database schema with table definitions

### CSV Exports
- `exports/csv/videos.csv` - Video metadata
- `exports/csv/tags.csv` - Unique tags
- `exports/csv/video_tags.csv` - Video-tag relationships
- `exports/csv/users.csv` - User information

### JSON Format
- `exports/json/` - JSON formatted data files

### Sample Data
- `samples/sample_1000.csv` - 1,000 video sample for quick exploration

See [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for detailed field descriptions.

## Ethical Considerations and Privacy

**Important**: This dataset was collected when YouTube's terms of service and privacy expectations were different from today. Users in 2006-2007 uploaded content and created tags with different privacy expectations than exist today.

### Responsible Use Guidelines

1. **Anonymization**: While usernames are historical public data, researchers should consider additional anonymization for publications
2. **Content Sensitivity**: Some videos may have been deleted or made private by users since collection
3. **Context Awareness**: Tagging behavior reflects 2006-2007 internet culture and norms
4. **Research Ethics**: Follow your institution's IRB guidelines for working with historical social media data

## Use Cases

This dataset is valuable for research in:

- **Information Science**: Folksonomy, user-generated metadata, collaborative tagging
- **Social Computing**: Early social media community practices
- **Digital History**: Internet culture and YouTube's formative period
- **Computational Linguistics**: Natural language use in tags, multilingual tagging
- **Information Retrieval**: Tag-based search and discovery
- **Cultural Studies**: Popular culture trends in late 2006/early 2007

## Citation

If you use this dataset in your research, please cite:

```bibtex
@misc{burns2006youtube,
  author = {Burns, Samuel A. and Geisler, Gary},
  title = {YouTube Tagging Dataset (2006-2007)},
  year = {2006-2007},
  note = {Dataset collected November 2006 - January 2007},
  url = {[DATASET URL]}
}
```

And please cite the associated research:

```bibtex
@inproceedings{geisler2007tagging,
  author = {Geisler, Gary and Burns, Sam},
  title = {Tagging Video: Conventions and Strategies of the YouTube Community},
  booktitle = {Proceedings of the Joint Conference on Digital Libraries (JCDL 2007)},
  year = {2007},
  pages = {480}
}
```

## License

This dataset is released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

**Attribution Requirements**:
- Cite the dataset and associated publications
- Acknowledge Samuel A. Burns and Gary Geisler as data collectors
- Note the collection period (2006-2007)

## Data Formats and Access

### Download Options

- **Complete MySQL Database** (637 MB): Full dataset in original MySQL format
- **CSV Export** (~XXX MB): Comma-separated values for easy import
- **JSON Export** (~XXX MB): JSON format for web applications
- **Sample Dataset** (~1 MB): 1,000 videos for testing and exploration

See [DOWNLOAD.md](docs/DOWNLOAD.md) for download links and checksums.

## Technical Details

### Database Schema
See [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for complete schema documentation.

### Working with MySQL Files

To restore the MySQL database:

```bash
# Extract the archive
tar -xzf youtube-database.tgz

# Start MySQL and create database
mysql -u root -p
CREATE DATABASE youtube_2006;
USE youtube_2006;

# If provided as SQL dump:
SOURCE youtube_2006.sql;

# If provided as data directory:
# Copy data files to MySQL data directory
# (method varies by MySQL version and configuration)
```

### Sample Queries

See [analysis/example_queries.sql](analysis/example_queries.sql) for useful SQL queries including:
- Most popular tags
- Tag co-occurrence analysis
- User upload patterns
- Tag diversity metrics

## Known Limitations

1. **Incomplete Coverage**: Dataset represents a sample of YouTube, not all videos from the period
2. **Deleted Content**: Many videos have likely been deleted or made private since collection
3. **API Limitations**: YouTube API v1 had limitations on data freshness and completeness
4. **Temporal Snapshot**: 3-month window may not capture seasonal variations
5. **Tag Relevance**: ~66% of tags had zero algorithmic relevance to video metadata (user-driven tagging)

## Version History

- **v1.0** (2025): Initial public release with documentation and multiple export formats
- **Original Collection** (2006-2007): Data collected for research project

## Contact

**Samuel A. Burns**  
School of Information  
The University of Texas at Austin  
sburns@ischool.utexas.edu

For questions about the dataset, research methodology, or technical issues, please contact the author.

## Acknowledgments

This dataset was collected with support from:
- The University of Texas at Austin School of Information
- Dr. Randolph Bias (research advisor)
- IBM Pervasive Computing Lab (research collaboration context)

Original research collaboration with Gary Geisler.

---

*This dataset represents an important snapshot of early YouTube community practices and is made available to support ongoing research in information science, social computing, and digital culture studies.*
