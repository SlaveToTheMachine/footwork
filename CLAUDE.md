# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RothBot Data Analysis is Month 1 of a 6-month project building a multimodal AI system that generates Van Halen songs. This phase focuses on analyzing 50 years of Van Halen's musical catalog to understand lyrical patterns, musical characteristics, and what makes their sound unique.

## Environment Setup

This project uses Python 3.10+ with a virtual environment:

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Required environment variables in `.env`:
- `GENIUS_ACCESS_TOKEN` - For fetching lyrics from Genius API
- `SPOTIFY_CLIENT_ID` - For Spotify API access
- `SPOTIFY_CLIENT_SECRET` - For Spotify API access
- `SPOTIFY_REDIRECT_URI` - OAuth redirect URI for Spotify

## Common Commands

### Running Jupyter Notebooks
```bash
# Start Jupyter
jupyter notebook

# Or use VS Code Jupyter extension
# Open notebooks/01_initial_exploration.ipynb directly
```

### Data Collection Scripts
```bash
# Fetch lyrics from Genius API (reads from van_halen_discography.csv)
cd scripts
python get_genius_lyrics.py

# Create Spotify playlist (example/testing script)
python spotify_playlist.py
```

## Architecture & Data Flow

### Data Pipeline

The project follows a CSV-driven workflow where `data/van_halen_discography.csv` is the **source of truth**:

1. **Source of Truth**: `data/van_halen_discography.csv`
   - Columns: `album_name`, `release_year`, `song_title`, `track_number`, `era`, `to_search`
   - The `to_search` column (TRUE/FALSE) controls which songs to fetch lyrics for
   - Eras: `DLR` (David Lee Roth) vs `HAGAR` (Sammy Hagar)

2. **Lyrics Collection**: `scripts/get_genius_lyrics.py`
   - Reads discography CSV, filters songs where `to_search=TRUE`
   - Uses `slugify()` function to normalize song titles to filenames
   - Outputs: Individual `.txt` files in `data/lyrics/` (one per song)
   - Also creates: `data/lyrics/van_halen_top_songs.json` (consolidated JSON)

3. **Analysis**: `notebooks/01_initial_exploration.ipynb`
   - Loads discography CSV with pandas
   - Loads lyrics using same `slugify()` function for filename matching
   - Performs lyrical analysis (word counts, common themes, vocabulary richness)
   - Visualizations of songs by era and release timeline

### Key Design Pattern: slugify()

Both the data collection script and analysis notebook use the same `slugify()` function to ensure filename consistency:

```python
def slugify(name: str) -> str:
    """Normalize song/title to filename: 'Hot for Teacher' -> 'hot_for_teacher'"""
    return re.sub(r'[_]+', '_', re.sub(r'\W+', '_', name)).strip('_').lower()
```

When working with lyrics data, always use this function to convert song titles to filenames.

### Directory Structure

```
data/
├── van_halen_discography.csv       # Source of truth for all songs
├── van_halen_discography_original.csv  # Backup (pre-fix)
├── lyrics/                         # Individual song lyrics (.txt files)
│   └── van_halen_top_songs.json   # Consolidated JSON
└── audio/                          # Future: Spotify audio features

scripts/
├── get_genius_lyrics.py           # Fetch lyrics from Genius API
├── spotify_playlist.py            # Spotify API integration (example)
└── csvread.py                     # Utility for CSV operations

notebooks/
└── 01_initial_exploration.ipynb   # Main analysis notebook
```

## Adding New Songs

To add songs to the analysis:

1. Edit `data/van_halen_discography.csv`
2. Add new row with song metadata
3. Set `to_search=TRUE` for songs you want lyrics for
4. Run `python scripts/get_genius_lyrics.py` to fetch lyrics
5. Re-run analysis notebook to include new songs

## Important Notes

- **Filename Consistency**: Always use the `slugify()` function when working with song titles/filenames to ensure the scripts and notebooks can find the correct files
- **Discography CSV is Source of Truth**: All song metadata lives in `van_halen_discography.csv`. Update this file first, then run collection scripts
- **Lyrics Storage**: Individual `.txt` files are preferred for analysis flexibility; the JSON file is supplementary
- **Era Analysis**: Songs are tagged with `DLR` or `HAGAR` era for comparison analysis between the two lead singers
