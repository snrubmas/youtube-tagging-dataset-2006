# Converting YouTube MySQL Database to Modern Formats

## Overview

You have a 637MB MySQL MyISAM database from 2006-2007. This guide helps you convert it to modern, accessible formats.

## Quick Start (Recommended Path)

### Step 1: Restore MySQL Database Temporarily

The easiest approach is to temporarily restore your MySQL database, then export it:

```bash
# 1. Extract your tgz file
tar -xzf youtube_database.tgz

# 2. Start MySQL (if not running)
sudo systemctl start mysql

# 3. Create database
mysql -u root -p
CREATE DATABASE youtube_2006;
EXIT;

# 4. Copy MySQL data files
# (Location varies by system - commonly /var/lib/mysql/)
sudo systemctl stop mysql
sudo cp -r extracted_database_dir /var/lib/mysql/youtube_2006
sudo chown -R mysql:mysql /var/lib/mysql/youtube_2006
sudo systemctl start mysql

# 5. Run the export script
python3 scripts/export_youtube_data.py \
    --mysql-user root \
    --mysql-password YOUR_PASSWORD \
    --mysql-db youtube_2006 \
    --output ./converted_data
```

This will create:
- ✅ `youtube_2006.db` - SQLite database (single file, no server needed)
- ✅ `videos.csv`, `tags.csv`, `video_tag_key.csv` - CSV files
- ✅ `*.jsonl` - JSON Lines files (one record per line)
- ✅ `*_sample_1000.json` - Small JSON samples for preview

### Step 2: Share the Converted Data

Upload the converted formats to your preferred hosting:
- University file server
- Zenodo (recommended for datasets - gets DOI)
- GitHub (if under 100MB, or use Git LFS)
- Figshare
- OSF (Open Science Framework)

## Alternative: Convert Without MySQL Server

If you can't restore MySQL, use the extraction script:

```bash
python3 scripts/convert_youtube_data.py youtube_database.tgz ./output
```

This will:
1. Extract the tgz
2. Scan the MySQL files
3. Create empty SQLite structure with correct schema
4. Generate instructions for data export

**Note**: This creates the structure but can't read the binary .MYD data without MySQL.

## Format Comparison

| Format | Best For | File Size | Pros | Cons |
|--------|----------|-----------|------|------|
| **SQLite** | General research | ~500MB | Single file, queryable, no server | Needs SQLite tools |
| **CSV** | Excel, R, simple analysis | ~800MB | Universal compatibility | No relationships, large |
| **JSONL** | Web apps, streaming | ~1GB | Easy to parse line-by-line | Larger size |
| **JSON** | Small samples, web apps | Use samples only | Human-readable | Too large for full dataset |
| **Parquet** | Big data, Python/R | ~300MB | Compressed, fast | Needs modern tools |

## Recommended Distribution Strategy

Create multiple download options:

### Full Dataset Package
```
youtube-tagging-dataset-2006/
├── youtube_2006.db          # SQLite (primary format)
├── csv/
│   ├── videos.csv
│   ├── tags.csv
│   └── video_tag_key.csv
└── samples/
    ├── videos_sample_1000.json
    ├── tags_sample_1000.json
    └── video_tag_key_sample_1000.json
```

### Sample Package (for quick exploration)
```
youtube-sample-1000/
├── videos_sample.csv
├── tags_sample.csv
├── video_tag_key_sample.csv
└── README.md
```

## Next Steps After Conversion

1. **Compress for distribution**:
   ```bash
   gzip videos.csv tags.csv video_tag_key.csv
   # Or create archives:
   tar -czf youtube_2006_csv.tar.gz csv/
   ```

2. **Calculate checksums**:
   ```bash
   sha256sum youtube_2006.db > checksums.txt
   sha256sum csv/*.csv >> checksums.txt
   ```

3. **Test the exports**:
   ```bash
   # Test SQLite
   sqlite3 youtube_2006.db "SELECT COUNT(*) FROM videos;"
   
   # Test CSV
   wc -l videos.csv
   ```

4. **Update your professional YAML**:
   Add this dataset as a major project/research output

5. **Create landing page** (we can build this):
   - Dataset description
   - Download links
   - Citation information
   - Sample queries

## Storage Size Estimates

Based on your 1M+ videos:
- MySQL (compressed): 637 MB
- SQLite: ~500-700 MB
- CSV (all files): ~800 MB - 1.2 GB
- CSV (gzipped): ~200-400 MB
- JSONL: ~1-1.5 GB
- JSONL (gzipped): ~300-500 MB

## Hosting Recommendations

**Best Options:**

1. **Zenodo** (recommended)
   - Free for academic datasets
   - Provides DOI (Digital Object Identifier)
   - Long-term preservation
   - No size limit for reasonable datasets
   - https://zenodo.org

2. **University Repository**
   - Contact UT Libraries
   - Texas Data Repository
   - Institutional support

3. **OSF (Open Science Framework)**
   - Free, academic-focused
   - Good for collaborative research
   - https://osf.io

4. **Figshare**
   - Free up to 20GB per file
   - Gets DOI
   - https://figshare.com

**Consider Multiple Mirrors:**
- Primary: Zenodo (authoritative, DOI)
- Mirror: University repository
- Samples: GitHub (for visibility)

## Questions to Answer Before Publishing

1. ✅ **License**: Creative Commons BY 4.0?
2. ✅ **Citation**: How should people cite it?
3. ⚠️ **Privacy**: Any user data concerns? (usernames were public)
4. ⚠️ **Ethics**: IRB considerations? (historical public data)
5. ✅ **Documentation**: README, data dictionary, examples
6. ✅ **Versioning**: This is v1.0

## Support Available

I can help you:
- ✅ Run the conversion scripts
- ✅ Create the landing page/documentation
- ✅ Generate sample datasets
- ✅ Write data analysis examples
- ✅ Update your professional YAML with this project
- ✅ Create citation information

## Troubleshooting

### "Can't connect to MySQL"
- Check MySQL is running: `sudo systemctl status mysql`
- Verify credentials
- Check database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### "Permission denied copying files"
- Use sudo: `sudo cp -r ...`
- Or change ownership first

### "Table doesn't exist after restore"
- Check files are in correct location
- Verify MySQL can see them: `SHOW TABLES;`
- Check MySQL error log: `sudo tail /var/log/mysql/error.log`

### "Export script fails"
- Install requirements: `pip install --break-system-packages mysql-connector-python`
- Check Python version: `python3 --version` (needs 3.6+)
- Run with full paths if relative paths fail

## Timeline Estimate

- Extract tgz: 1-2 minutes
- Restore to MySQL: 5-10 minutes
- Export all formats: 30-60 minutes (depending on system)
- Compress for distribution: 10-20 minutes
- Upload to Zenodo: 20-60 minutes (depending on connection)

**Total: 1-2 hours of active work**

---

Ready to get started? Let me know which path you want to take!
