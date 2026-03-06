# Football Match Analysis - StatsBomb Data Visualizations
## Team-11 Project 2

**Team Members:**
- Sashangh DR - 2024101069
- Arun K - 2025121004
- Aayush Khatanhar - 2024101131

---

## 📊 Project Overview

This project creates three interactive D3.js visualizations analyzing football match dynamics using StatsBomb event-level data:

1. **Turnover Locations with Grid Heatmap** - Identifies where teams lose possession with intensity zones
2. **Shot Origin and xG Analysis** - Maps shooting opportunities sized by expected goals (xG) value
3. **Defensive Actions by Zone** - Visualizes defensive organization across pitch thirds

---

## 🚀 How to Run the Visualizations

### Prerequisites

- Python 3.x installed on your system
- A modern web browser (Chrome, Firefox, Edge, Safari)
- The `open-data` folder is already included in this project

### Step 1: Process Match Data

The StatsBomb open-data folder contains hundreds of match files. You need to process one match at a time.

**Command:**
```bash
python process_statsbomb_data.py --events_path ./open-data/data/events/MATCH_ID.json --output_dir ./processed_data
```

**Replace `MATCH_ID` with any match file from the `open-data/data/events/` folder.**

**Example:**
```bash
python process_statsbomb_data.py --events_path ./open-data/data/events/3888787.json --output_dir ./processed_data
```

This will:
- Extract turnovers, shots, and defensive actions from the match
- Create/update files in the `processed_data/` folder:
  - `turnovers.json`
  - `shots.json`
  - `defensive_actions.json`
  - `metadata.json`
  - `combined_data.json` ← This is what you'll upload

### Step 2: Open the Visualization

1. Double-click `football_visualizations.html` to open it in your browser
   - Or right-click → Open with → Chrome/Firefox

2. You'll see three empty visualizations with sample data

### Step 3: Load Your Processed Data

1. Click the **"Upload StatsBomb JSON"** button at the top
2. Navigate to the `processed_data/` folder
3. Select `combined_data.json`
4. Click **Open**

**The visualizations will instantly update with your match data!**

### Step 4: Explore the Visualizations

- **Hover** over any element to see detailed information
- **Click** legend items to show/hide specific event types
- Use the **Team filter** dropdown to view individual team statistics

---

## 📂 Finding Match IDs

To find interesting matches, browse the `open-data/data/events/` folder. Each JSON file is a match.

**Quick examples from the folder:**
```
15946.json
19714.json
3888787.json
303731.json
```

You can also check `open-data/data/matches/` to see match details like team names and competition.

---

## 🎨 Visualization Details

### 1. Turnover Locations Visualization

**What it shows:**
- **Grid Heatmap**: 10x10 grid showing turnover density (red intensity = more turnovers)
- **Scatter Points**: Each circle is one turnover event
- **Color-coded by type**: Miscontrol, Dispossessed, Duel Lost, Pass Intercepted, Bad Touch, Error

**How to use:**
- Hover over grid cells to see zone statistics
- Hover over circles for player/team/minute details
- Click legend items to filter by turnover type
- Red intensity shows structural vulnerabilities

---

### 2. Shot Origin and xG Visualization

**What it shows:**
- **Circle size** = Expected Goals (xG) value (larger = better chance)
- **Colors** = Shot outcome (Green=Goal, Blue=Saved, Gray=Blocked, Orange=Off Target, Yellow=Post)
- **Golden borders** highlight goals
- **xG reference circles** at bottom show size scale (10%, 50%, 90%)

**How to use:**
- Hover over circles for xG value and shooter details
- Click legend to filter by shot outcome
- Identify attacking patterns and dangerous zones
- Compare shot quality across different areas

---

### 3. Defensive Actions by Zone Visualization

**What it shows:**
- **Three pitch zones**: Defensive Third (pink), Middle Third (yellow), Attacking Third (green)
- **Letter indicators** inside circles show action type:
  - **P** = Pressure
  - **T** = Tackle
  - **I** = Interception
  - **B** = Block
  - **R** = Ball Recovery
  - **C** = Clearance
  - **D** = Duel
- **Border colors**: Green = successful, Red = failed

**How to use:**
- Hover over circles for action details
- Click legend to filter by action type
- Analyze defensive shape and pressing patterns
- Zone labels show territorial defensive strategy

---

## 📁 Project Structure

```
DV PROJECT-2/
│
├── football_visualizations.html    # Main dashboard (open this!)
├── process_statsbomb_data.py       # Data processing script
├── README.md                       # This file
│
├── open-data/                      # StatsBomb dataset (included)
│   └── data/
│       ├── competitions.json
│       ├── matches/
│       └── events/                 # Match files here (use these IDs)
│           ├── 15946.json
│           ├── 19714.json
│           ├── 3888787.json
│           └── ... (hundreds more)
│
└── processed_data/                 # Generated after running script
    ├── turnovers.json
    ├── shots.json
    ├── defensive_actions.json
    ├── metadata.json
    └── combined_data.json          # Upload this file!
```

---

## 🎯 Quick Workflow Summary

1. **Pick a match** from `open-data/data/events/` (e.g., `3888787.json`)
2. **Run command**: `python process_statsbomb_data.py --events_path ./open-data/data/events/3888787.json --output_dir ./processed_data`
3. **Open** `football_visualizations.html` in browser
4. **Upload** `processed_data/combined_data.json`
5. **Explore** the interactive visualizations!

---

## 💡 Tips

- Process different matches to compare team performances
- The visualization remembers your last upload
- All interactions are client-side (no server needed)
- Works offline once the HTML file is loaded
- Legend items are clickable for filtering
- Team selector dynamically updates based on uploaded data

---

## 🛠️ Troubleshooting

**"No data loaded" error:**
- Make sure you ran the Python script first
- Check that `combined_data.json` exists in `processed_data/`
- Verify the JSON file is not empty

**Visualizations not updating:**
- Press Ctrl+F5 (Windows) or Cmd+Shift+R (Mac) to hard refresh
- Make sure you selected `combined_data.json` (not individual files)

**Python script errors:**
- Ensure Python 3.x is installed: `python --version`
- Check that the match ID file exists in `open-data/data/events/`

**File upload button not responding:**
- Try a different browser (Chrome recommended)
- Check browser console (F12) for errors

---

## 📊 Data Source

All match data comes from **StatsBomb Open Data**, a free resource providing detailed event-level football data.

Repository: https://github.com/statsbomb/open-data

The `open-data` folder in this project contains the complete dataset with:
- 10+ competitions (World Cup, La Liga, Premier League, etc.)
- Hundreds of matches
- Detailed event data (passes, shots, tackles, etc.)

---

## 🎓 Technical Details

**Built with:**
- D3.js v7 (core visualization library)
- D3 Contour Plugin (for heatmaps)
- Vanilla JavaScript (no frameworks)
- HTML5 + CSS3
- Python 3 (data processing)

**Features:**
- Responsive SVG graphics
- Interactive tooltips
- Click-to-filter legends
- Team-specific filtering
- Real-time data updates
- Boundary-clamped visualizations (no overflow!)

---

## 📝 License

This project uses StatsBomb Open Data which is free for public use with proper attribution.

---

## 🙋 Support

For questions or issues, contact the team members listed at the top of this document.

**Enjoy exploring football analytics!** ⚽📈
