-- Example SQL Queries for YouTube Tagging Dataset
-- 
-- These queries demonstrate common analysis patterns using the dataset.
-- Run these against youtube_2006.db using sqlite3 or any SQLite tool.

-- ===========================================================================
-- Top 10 Most Frequently Used Tags
-- ===========================================================================
-- Shows which tags were most popular in the YouTube community
SELECT t.tag, COUNT(*) as usage_count
FROM tags t
JOIN video_tag_key vtk ON t.tag_id = vtk.tag_id
GROUP BY t.tag_id, t.tag
ORDER BY usage_count DESC
LIMIT 10;

-- ===========================================================================
-- Videos Per User Distribution
-- ===========================================================================
-- Shows the most prolific uploaders in the dataset
SELECT author, COUNT(*) as video_count
FROM videos
GROUP BY author
ORDER BY video_count DESC
LIMIT 20;

-- ===========================================================================
-- Tags Per Video Statistics
-- ===========================================================================
-- Distribution showing how many videos have 1 tag, 2 tags, 3 tags, etc.
SELECT 
    tags_per_video,
    COUNT(DISTINCT vid_id) as video_count
FROM (
    SELECT vid_id, COUNT(*) as tags_per_video
    FROM video_tag_key
    GROUP BY vid_id
) as tag_counts
GROUP BY tags_per_video
ORDER BY tags_per_video;

-- ===========================================================================
-- Most Viewed Videos
-- ===========================================================================
SELECT vid_id, title, author, view_count
FROM videos
ORDER BY view_count DESC
LIMIT 20;

-- ===========================================================================
-- Videos by Upload Date
-- ===========================================================================
-- Shows video upload activity over time
SELECT 
    DATE(upload_time, 'unixepoch') as upload_date,
    COUNT(*) as videos_uploaded
FROM videos
GROUP BY upload_date
ORDER BY upload_date;

-- ===========================================================================
-- Tag Co-occurrence
-- ===========================================================================
-- Find which tags frequently appear together on the same videos
SELECT 
    t1.tag as tag1,
    t2.tag as tag2,
    COUNT(*) as co_occurrence_count
FROM video_tag_key vtk1
JOIN video_tag_key vtk2 ON vtk1.vid_id = vtk2.vid_id
JOIN tags t1 ON vtk1.tag_id = t1.tag_id
JOIN tags t2 ON vtk2.tag_id = t2.tag_id
WHERE vtk1.tag_id < vtk2.tag_id
GROUP BY t1.tag_id, t2.tag_id
ORDER BY co_occurrence_count DESC
LIMIT 20;

-- ===========================================================================
-- Average Rating by Number of Tags
-- ===========================================================================
-- Does using more tags correlate with higher ratings?
SELECT 
    tag_count,
    AVG(rating_avg) as avg_rating,
    COUNT(*) as video_count
FROM (
    SELECT 
        v.vid_id,
        v.rating_avg,
        COUNT(vtk.tag_id) as tag_count
    FROM videos v
    LEFT JOIN video_tag_key vtk ON v.vid_id = vtk.vid_id
    WHERE v.rating_avg IS NOT NULL
    GROUP BY v.vid_id
) as video_stats
GROUP BY tag_count
ORDER BY tag_count;

-- ===========================================================================
-- Case Sensitivity in Tags
-- ===========================================================================
-- Shows how the same word appears with different capitalization
SELECT tag, COUNT(*) as usage_count
FROM tags
WHERE LOWER(tag) = 'music'
ORDER BY usage_count DESC;
