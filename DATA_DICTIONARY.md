# YouTube Tagging Dataset - Data Dictionary

## Database Schema

### Table: videos
- `vid_id` (TEXT) - YouTube video identifier (primary key)
- `title` (TEXT) - Video title
- `author` (TEXT) - Username of uploader
- `length_seconds` (INTEGER) - Video duration
- `rating_avg` (REAL) - Average rating (1-5 scale)
- `rating_count` (INTEGER) - Number of ratings
- `description` (TEXT) - Video description
- `view_count` (INTEGER) - Number of views at collection time
- `upload_time` (INTEGER) - Unix timestamp of upload
- `comment_count` (INTEGER) - Number of comments
- `url` (TEXT) - YouTube video URL
- `thumbnail_url` (TEXT) - Video thumbnail URL
- `created` (TEXT) - Record creation date
- `modified` (TEXT) - Record modification date

### Table: tags
- `tag_id` (INTEGER) - Internal tag identifier (primary key)
- `tag` (TEXT) - Tag text/string
- `created` (TEXT) - Record creation date
- `modified` (TEXT) - Record modification date
- `looked_up` (INTEGER) - Flag indicating if tag was processed

### Table: video_tag_key
- `vid_id` (TEXT) - Video identifier (foreign key)
- `tag_id` (INTEGER) - Tag identifier (foreign key)
- `created` (TEXT) - Relationship creation date
- Composite primary key: (vid_id, tag_id)

## Data Characteristics

- **Case Sensitivity**: Tags preserve case (e.g., "black" vs "Black")
- **Special Characters**: Tags may begin with quotes, parentheses, etc.
- **Encoding**: UTF-8
- **NULL Values**: Some fields may contain NULL
- **Date Formats**: 
  - `upload_time`: Unix timestamp (seconds since 1970-01-01)
  - `created`/`modified`: YYYY-MM-DD HH:MM:SS format

## File Formats

### SQLite Database
- **File**: `youtube_2006.db`
- **Size**: ~1.1 GB
- **Use**: Query with any SQLite tool
- **Example**: `sqlite3 youtube_2006.db "SELECT * FROM videos LIMIT 10;"`

### CSV Files
- **Files**: `videos.csv`, `tags.csv`, `video_tag_key.csv`
- **Total Size**: ~603 MB
- **Encoding**: UTF-8
- **Delimiter**: Comma
- **Quote**: Double quote
- **Headers**: First row contains column names
- **Note**: Some videos.csv rows may have embedded newlines in descriptions

### JSON Lines (JSONL)
- **Files**: `videos.jsonl`, `tags.jsonl`, `video_tag_key.jsonl`
- **Format**: One JSON object per line
- **Use**: Stream processing, web applications
- **Example**: `jq -c '.title' videos.jsonl | head -10`

### Sample Files
- **Files**: `*_sample_1000.json`
- **Format**: Standard JSON array
- **Size**: 1,000 records each
- **Use**: Quick preview, testing code

## Known Issues

1. **Unescaped Quotes**: Some video descriptions contain unescaped quotes
2. **Deleted Videos**: Many videos have been deleted since 2006-2007
3. **URLs**: Original YouTube URLs may no longer work
4. **Thumbnails**: Thumbnail URLs are historical and may not resolve

## Example Queries

### SQLite
```sql
-- Top 10 most tagged videos
SELECT v.title, COUNT(vtk.tag_id) as tag_count
FROM videos v
JOIN video_tag_key vtk ON v.vid_id = vtk.vid_id
GROUP BY v.vid_id
ORDER BY tag_count DESC
LIMIT 10;

-- Most popular tags
SELECT t.tag, COUNT(vtk.vid_id) as usage_count
FROM tags t
JOIN video_tag_key vtk ON t.tag_id = vtk.tag_id
GROUP BY t.tag_id
ORDER BY usage_count DESC
LIMIT 20;

-- Videos per user
SELECT author, COUNT(*) as video_count
FROM videos
GROUP BY author
ORDER BY video_count DESC
LIMIT 10;
```

## Citation

If you use this dataset, please cite:

**Dataset:**
Burns, S. & Geisler, G. (2006-2007). YouTube Tagging Dataset. 
DOI: 10.5281/zenodo.17508119

**Related Publication:**
Geisler, G., & Burns, S. (2007). Tagging video: Conventions and strategies 
of the YouTube community. In Proceedings of the 7th ACM/IEEE-CS joint 
conference on Digital libraries (p. 480). 
DOI: 10.1145/1255175.1255279
