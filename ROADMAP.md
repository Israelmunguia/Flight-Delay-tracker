
### Project Setup
- [x] Create GitHub repository and add team members
- [x] Write and finalize README.md
- [x] Add this ROADMAP.md file
- [x] Download database
### Environment & Tools
- [x]Create and activate virtual environment (python -m venv .venv)
-[x]Install core libraries: pandas, matplotlib (add others later)
-[x] Verify script runs
-[x]First commits pushed (at least 2–3 small commits)
### Planning
-[x] Define initial goal:“Summarize basic delay reasons and visualize them.”
-[x] List core data columns needed (depdelay, carrierdelay, etc.)
### Data Handling
-[x] Place raw CSV in input/ folder
-[x] Write basic load script (flight_delay_analysis.py)
-[] Lowercase all column names
-[] Identify which expected delay columns actually exist
-[] Handle missing values in delay columns (fill with 0)
-[] Convert delay columns to integer safely
-[] Decide how to treat negative departure delays (clip to 0)
-[] Add simple error message if file not found or columns missing