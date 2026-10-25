# Sources — Story 4

## Primary statistical source
U.S. Bureau of Labor Statistics (BLS), Occupational Employment and Wage Statistics (OEWS), May 2025.
- Official tables: https://www.bls.gov/oes/tables.htm
- Documentation: https://www.bls.gov/oes/oes_doc.htm

## Actual table pages used in this project
The included state-wage figures were transcribed from these third-party BLS-attributed occupation pages, **not directly downloaded from BLS**:
- Data Scientists (15-2051): https://signalbleed.com/jobs/data-scientists.html
- Database Architects (15-1243): https://signalbleed.com/jobs/database-architects.html
- Database Administrators (15-1242): https://signalbleed.com/jobs/database-administrators.html
- Computer Systems Analysts (15-1211): https://signalbleed.com/jobs/computer-systems-analysts.html
- Operations Research Analysts (15-2031): https://signalbleed.com/jobs/operations-research-analysts.html
- Statisticians (15-2041): https://signalbleed.com/jobs/statisticians.html

## Data scope and caveats
- Wages are annual **means**, nominal dollars, and are not cost-of-living adjusted.
- The six-occupation comparison contains 16 **selected states** (not all U.S. states).
- Data Scientists geographic comparison has 49 published state/DC entries.
- One state×occupation mean wage was unavailable, retained as missing.
- Role titles like Data Engineer and Business Analyst cannot automatically be equated with BLS SOC categories.
- Data in `data/processed/` represent the curated source tables; `data/raw/` is intentionally empty because official raw OEWS tables were not obtained.
