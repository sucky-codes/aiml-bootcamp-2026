# AIML Bootcamp 2026 🚀

Welcome to my AIML Bootcamp 2026 repository!

I'm a student participating in the Machine Learning Bootcamp conducted by Soham Bhattacharya and presented by GLA University, Mathura. This repository tracks my learning journey through mini projects completed during the program.

---

## 🕷️ Web Scraper Module (`web_scraping.py`)

A modular, production-ready Python web scraper featuring automated HTTP request handling, custom User-Agent headers, page pagination, HTML element parsing with `BeautifulSoup4`, and clean data export to CSV/JSON via `pandas`.

### ✨ Key Features
- **Smart Parsing**: Automated extraction of content, authors/sources, tags, text, and metadata.
- **Bot Protection Evasion**: Spoofed User-Agent headers and customizable request rate-limiting delays.
- **Pagination Support**: Automatically detects and follows "Next Page" links up to a configured limit.
- **Flexible Export Formats**: Export structured data directly to `.csv` or `.json` formats.
- **Command Line Interface (CLI)**: Full command-line configuration for URLs, output files, page limits, and request throttling.

### 📦 Prerequisites & Installation
1. Ensure Python 3.8+ is installed on your system.
2. Install the required dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 🚀 Usage Examples

#### Run default scrape (Quotes target, outputting to CSV):
```bash
python web_scraping.py
```

#### Scrape a custom URL with JSON output and max 5 pages:
```bash
python web_scraping.py --url "http://quotes.toscrape.com" --output "quotes.json" --format json --max-pages 5 --delay 1.5
```

#### Command Line Options
| Option | Short Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| `--url` | `-u` | `http://quotes.toscrape.com` | Target URL to scrape |
| `--output` | `-o` | `scraped_data.csv` | Output file path |
| `--format` | `-f` | `csv` | Export format (`csv` or `json`) |
| `--max-pages` | `-p` | `2` | Maximum number of pages to scrape |
| `--delay` | `-d` | `1.0` | Delay between consecutive HTTP requests (seconds) |

---

## 📚 Topics Covered in Repo
- **Python for AI/ML & Web Scraping**
- **Data Analysis & Processing with Pandas**
- **Machine Learning & Model Evaluation**
- **Real-World Projects & Data Pipelines**

---

## 🎯 Purpose
To document my progress, practice machine learning and data engineering concepts, and build a strong technical portfolio throughout the bootcamp.
