# AI Exposure of the India Job Market

Analyzing how susceptible every occupation in the Indian economy is to AI and automation, using data from India's **National Classification of Occupations (NCO)** and the **Periodic Labour Force Survey (PLFS)** published by the Ministry of Labour & Employment.

![AI Exposure Treemap](jobs.png)

## What's here

The NCO covers hundreds of occupations spanning every sector of the Indian economy, with detailed data on job duties, education requirements, employment, and growth projections. We compile occupation data from official Indian government sources, score each occupation's AI exposure using an LLM, and build an interactive treemap visualization.

## Data Sources (India)

Unlike the US version (which uses the BLS Occupational Outlook Handbook), this India adaptation uses:

- **[National Classification of Occupations (NCO-2015)](https://labour.gov.in/sites/default/files/NCO-2015.pdf)** — India's official occupation classification, published by the Ministry of Labour & Employment, organized by NIC sectors
- - **[Periodic Labour Force Survey (PLFS)](https://mospi.gov.in/web/plfs)** — Annual survey by MoSPI providing employment counts by occupation and sector
  - - **[India Skills Report](https://wheebox.com/india-skills-report.htm)** — Sector-level employability and skills data
    - - **[National Occupational Standards (NOS)](https://www.nqr.gov.in/)** — Detailed occupation descriptions from the National Skill Development Corporation (NSDC)
     
      - ## Data pipeline
     
      - 1. **Scrape** (`scrape.py`) — Downloads raw HTML/PDF data for occupation pages from official Indian government sources (NCO, NOS, PLFS) into `html/`.
        2. 2. **Parse** (`parse_detail.py`, `process.py`) — Converts raw HTML into clean Markdown files in `pages/`.
           3. 3. **Tabulate** (`make_csv.py`) — Extracts structured fields (pay, education, job count, growth outlook, NIC code) into `occupations.csv`.
              4. 4. **Score** (`score.py`) — Sends each occupation's Markdown description to an LLM (Gemini Flash via OpenRouter) with a scoring rubric calibrated for the Indian context. Each occupation gets an AI Exposure score from 0-10 with a rationale. Results saved to `scores.json`.
                 5. 5. **Build site data** (`build_site_data.py`) — Merges CSV stats and AI exposure scores into a compact `site/data.json` for the frontend.
                    6. 6. **Website** (`site/index.html`) — Interactive treemap visualization where area = employment and color = AI exposure (green to red).
                      
                       7. ## Key files
                      
                       8. | File | Description |
                       9. |------|-------------|
                       10. | `occupations.json` | Master list of occupations with title, URL, category, slug |
                       11. | `occupations.csv` | Summary stats: pay, education, job count, growth projections |
                       12. | `scores.json` | AI exposure scores (0-10) with rationales for all occupations |
                       13. | `prompt.md` | All data in a single file, designed to be pasted into an LLM for analysis |
                       14. | `html/` | Raw HTML pages from government sources (source of truth) |
                       15. | `pages/` | Clean Markdown versions of each occupation page |
                       16. | `site/` | Static website (treemap visualization) |
                      
                       17. ## AI exposure scoring
                      
                       18. Each occupation is scored on a single **AI Exposure** axis from 0 to 10, measuring how much AI will reshape that occupation in the **Indian context**. The score considers both direct automation (AI doing the work) and indirect effects (AI making workers so productive that fewer are needed), accounting for India-specific factors such as:
                      
                       19. - India's large informal economy and prevalence of manual labor
                           - - Lower average wage levels making automation economics different
                             - - Rapid digitization in IT, fintech, and service sectors
                               - - High concentration of employment in agriculture and construction
                                
                                 - A key signal is whether the job's work product is fundamentally digital. Jobs in India's large IT/BPO sector face very high exposure, while jobs in agriculture, construction, and informal services have greater resilience.
                                
                                 - **Calibration examples for the Indian market:**
                                
                                 - | Score | Meaning | Examples |
                                 - |-------|---------|---------|
                                 - | 0-1 | Minimal | Agricultural laborers, brick kiln workers, construction laborers |
                                 - | 2-3 | Low | Electricians, plumbers, ASHA workers, security guards |
                                 - | 4-5 | Moderate | Nurses, retail workers, primary school teachers |
                                 - | 6-7 | High | Bank officers, chartered accountants, engineers, managers |
                                 - | 8-9 | Very high | Software developers, BPO agents, data entry operators, paralegals |
                                 - | 10 | Maximum | Medical transcriptionists, basic data entry clerks |
                                
                                 - ## Visualization
                                
                                 - The main visualization is an interactive **treemap** where:
                                 - - **Area** of each rectangle is proportional to employment (number of jobs)
                                   - - **Color** indicates AI exposure on a green (safe) to red (exposed) scale
                                     - - **Layout** groups occupations by NCO category / NIC sector
                                       - - **Hover** shows detailed tooltip with pay, jobs, outlook, education, exposure score, and LLM rationale
                                        
                                         - ## Setup
                                        
                                         - ```
                                           uv sync
                                           uv run playwright install chromium
                                           ```

                                           Requires an OpenRouter API key in `.env`:

                                           ```
                                           OPENROUTER_API_KEY=your_key_here
                                           ```

                                           ## Usage

                                           ```bash
                                           # Scrape occupation pages (only needed once, results are cached in html/)
                                           uv run python scrape.py

                                           # Generate Markdown from HTML
                                           uv run python process.py

                                           # Generate CSV summary
                                           uv run python make_csv.py

                                           # Score AI exposure (uses OpenRouter API)
                                           uv run python score.py

                                           # Build website data
                                           uv run python build_site_data.py

                                           # Serve the site locally
                                           cd site && python -m http.server 8000
                                           ```

                                           ## Differences from the US version

                                           | Aspect | US (karpathy/jobs) | India (this repo) |
                                           |--------|-------------------|-------------------|
                                           | Data source | BLS Occupational Outlook Handbook | NCO-2015 + PLFS + NOS |
                                           | # Occupations | 342 | ~400+ NCO categories |
                                           | Pay data | USD median annual salary | INR average annual earnings |
                                           | Employment projections | BLS 10-year outlook | PLFS + sector growth estimates |
                                           | Occupation structure | BLS SOC codes | NCO NIC codes |
                                           | Scraping target | bls.gov/ooh | labour.gov.in / nqr.gov.in |
