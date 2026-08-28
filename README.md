<!--
README.md - South Africa Data Analysis Project
A professional data science portfolio project
-->

<div align="center">

# 🇿🇦 South Africa Data Analysis Project

### 📊 Unemployment & Tertiary Education Trends (1991-2023)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://south-africa-data-analysis.streamlit.app)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Key Findings](#-key-findings)
- [Data Sources](#-data-sources)
- [Methodology](#-methodology)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dashboard](#-interactive-dashboard)
- [Visualizations](#-visualizations)
- [Statistical Analysis](#-statistical-analysis)
- [Database](#-database)
- [Technologies Used](#-technologies-used)
- [Future Work](#-future-work)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

This project analyzes the relationship between **unemployment rates** and **tertiary education enrolment** in South Africa over three decades (1991-2023). Using data from the World Bank Development Indicators, the analysis reveals a strong positive correlation that challenges conventional assumptions about education and employment.

### The Research Question

> *"Does higher education automatically lead to lower unemployment?"*

Our findings show a **counterintuitive relationship** in South Africa's context, suggesting structural issues in the labor market that require policy attention.

---

## 🚀 Live Demo

Experience the interactive dashboard live:

**[🔗 View Live Dashboard](https://south-africa-data-analysis.streamlit.app)**

---

## 🔍 Key Findings

### 📈 Unemployment Trends
| Metric | Value |
|--------|-------|
| **Mean Unemployment Rate** | 26.87% |
| **Lowest (1994)** | 23.07% |
| **Highest (2021)** | 34.01% |
| **Trend** | ↑ Increasing over time |

### 🎓 Education Trends
| Metric | Value |
|--------|-------|
| **Mean Tertiary Enrolment** | 19.02% |
| **Lowest (1991)** | 11.85% |
| **Highest (2022)** | 23.73% |
| **Trend** | ↑ Doubled over time |

### 🔗 The Relationship
| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Pearson Correlation** | 0.831 | Strong positive relationship |
| **P-value** | < 0.001 | Statistically significant |
| **R-squared** | 0.691 | 69% of variance explained |
| **Regression Equation** | U = 12.25 + 0.77E | Each 1% education increase → 0.77% unemployment increase |

### 💡 Key Insight
> *"Education expansion alone may not reduce unemployment without corresponding job creation and structural reforms."*

---

## 📦 Data Sources

| Indicator | Code | Source | Description |
|-----------|------|--------|-------------|
| Unemployment Rate | `SL.UEM.TOTL.ZS` | World Bank / ILO | Modeled ILO unemployment rate, % of total labor force |
| Tertiary Enrolment | `SE.TER.ENRR` | World Bank / UNESCO | Gross tertiary enrolment ratio, % of age-appropriate population |

**Data Coverage:** South Africa, 1991-2023 (16 valid observations)

---

## ⚙️ Methodology

### Pipeline Overview
┌─────────────────┐
│ World Bank API │
│ (Data Source) │
└────────┬────────┘
▼
┌─────────────────┐
│ Download Data │
│ (requests) │
└────────┬────────┘
▼
┌─────────────────┐
│ Data Cleaning │
│ (pandas) │
└────────┬────────┘
▼
┌─────────────────┐
│ EDA & Analysis │
│ (statistics) │
└────────┬────────┘
▼
┌─────────────────┐
│ SQLite Database│
│ (storage) │
└────────┬────────┘
▼
┌─────────────────┐
│ Visualizations │
│ (matplotlib) │
└────────┬────────┘
▼
┌─────────────────┐
│ Dashboard │
│ (Streamlit) │
└─────────────────┘

text

### Analysis Steps

1. **Data Collection**: Automated download from World Bank API
2. **Data Cleaning**: Remove missing values, standardize formats
3. **Exploratory Analysis**: Visual and statistical exploration
4. **Statistical Modeling**: Correlation analysis and linear regression
5. **Database Storage**: SQLite for structured querying
6. **Dashboard Development**: Interactive visualization with Streamlit

---

## 📁 Project Structure
SouthAfrica-Data-Analysis/
│
├── 📊 data/
│ ├── raw/ # Raw data from World Bank
│ │ ├── south_africa_unemployment.csv
│ │ └── south_africa_tertiary_education.csv
│ └── processed/ # Cleaned and merged data
│ └── south_africa_combined.csv
│
├── 🗄️ database/
│ ├── south_africa_data.db # SQLite database
│ ├── south_africa_data_export.csv # Exported data
│ └── database_summary.csv # Summary statistics
│
├── 📓 notebooks/
│ └── 01_data_inspection.ipynb # Jupyter notebook
│
├── 📈 outputs/
│ ├── figures/ # Visualizations
│ │ ├── correlation_analysis.png
│ │ ├── distributions.png
│ │ ├── regression_analysis.png
│ │ ├── time_series.png
│ │ └── time_series_analysis.png
│ ├── reports/ # Analysis reports
│ │ ├── eda_report.txt
│ │ └── statistical_analysis_report.txt
│ └── tables/
│ └── summary_statistics.csv
│
├── 💻 src/ # Python scripts
│ ├── download_data.py # Download from World Bank
│ ├── data_cleaning.py # Clean and merge data
│ ├── exploratory_analysis.py # EDA and visualizations
│ ├── statistical_analysis_simple.py # Statistical analysis
│ └── create_database.py # Build SQLite database
│
├── 🎯 dashboard/
│ └── app.py # Streamlit dashboard
│
├── 🐍 .venv/ # Virtual environment
├── 📋 requirements.txt # Dependencies
├── 📄 LICENSE # MIT License
└── 📖 README.md # This file

text

---

## 🔧 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git (for version control)

### Step 1: Clone the Repository

```bash
git clone https://github.com/mxolisi78/south-africa-data-analysis.git
cd south-africa-data-analysis
Step 2: Create Virtual Environment
bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Run the Full Pipeline
bash
# Download data
python src/download_data.py

# Clean and merge
python src/data_cleaning.py

# Run exploratory analysis
python src/exploratory_analysis.py

# Perform statistical analysis
python src/statistical_analysis_simple.py

# Create database
python src/create_database.py
🚀 Usage
Run the Full Analysis Pipeline
bash
python src/download_data.py && \
python src/data_cleaning.py && \
python src/exploratory_analysis.py && \
python src/statistical_analysis_simple.py && \
python src/create_database.py
Launch the Interactive Dashboard Locally
bash
streamlit run dashboard/app.py
Then open your browser to: http://localhost:8501

Query the Database
bash
sqlite3 database/south_africa_data.db

# SQL queries
SELECT * FROM south_africa_data;
SELECT AVG(unemployment_rate) FROM south_africa_data;
.quit
🎨 Interactive Dashboard
The dashboard provides an interactive way to explore the data:

Features
Feature	Description
Year Range Filter	Select specific year ranges for analysis
Key Metrics	Display average unemployment and enrolment
Trend Charts	Line charts showing historical trends
Combined View	Both indicators on one graph
Scatter Plot	Relationship visualization with correlation
Data Table	View and interact with raw data
Download	Export data as CSV
Dashboard Sections
📊 Key Metrics - Quick stats at a glance

📈 Trend Analysis - Historical trends over time

🔗 Relationship Analysis - Correlation visualization

📋 Data Explorer - Interactive data table

📊 Visualizations
1. Time Series Analysis
Unemployment rate trend (1991-2023)

Tertiary enrolment trend (1991-2023)

Moving averages and year-over-year changes

2. Correlation Analysis
Correlation heatmap

Scatter plot with regression line

Residual analysis

3. Distribution Analysis
Histograms with kernel density estimates

Mean and median indicators

4. Statistical Visualizations
Regression diagnostics

Trendline with confidence intervals

📈 Statistical Analysis
Correlation Analysis
python
Pearson Correlation: 0.8314 (p < 0.001)
Spearman Correlation: 0.8298 (p < 0.001)
Interpretation: Strong, statistically significant positive correlation between education and unemployment.

Regression Analysis
text
R-squared: 0.6912
Adjusted R-squared: 0.6691
RMSE: 1.9476

Unemployment = 12.2467 + 0.7686 * Enrolment
Interpretation: The model explains 69% of the variance in unemployment rates.

Time Series Findings
Metric	Unemployment	Education
Total Change	+8.96%	+11.65%
Average Growth	+0.29%/year	+0.38%/year
Max Value	34.01% (2021)	23.73% (2022)
Min Value	23.07% (1994)	11.85% (1991)
🗄️ Database
Schema
sql
CREATE TABLE south_africa_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    unemployment_rate REAL,
    tertiary_enrolment REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Example Queries
sql
-- Get all data
SELECT * FROM south_africa_data ORDER BY year;

-- Summary statistics
SELECT 
    COUNT(*) as total_records,
    MIN(year) as min_year,
    MAX(year) as max_year,
    ROUND(AVG(unemployment_rate), 2) as avg_unemployment,
    ROUND(AVG(tertiary_enrolment), 2) as avg_enrolment
FROM south_africa_data;

-- Years with unemployment > 30%
SELECT year, unemployment_rate 
FROM south_africa_data 
WHERE unemployment_rate > 30;
Indexes
sql
CREATE INDEX idx_year ON south_africa_data(year);
CREATE INDEX idx_unemployment ON south_africa_data(unemployment_rate);
CREATE INDEX idx_enrolment ON south_africa_data(tertiary_enrolment);
🛠️ Technologies Used
Core Technologies
Technology	Purpose
Python	Programming language
Pandas	Data manipulation
NumPy	Numerical computing
Matplotlib	Data visualization
Seaborn	Statistical visualization
Scipy	Statistical tests
Data & Storage
Technology	Purpose
SQLite	Lightweight database
Requests	API requests
World Bank API	Data source
Dashboard & UI
Technology	Purpose
Streamlit	Dashboard framework
Plotly	Interactive visualizations
🔮 Future Work
Short-term Enhancements
□ Add more World Bank indicators (GDP, inflation, poverty)
□ Include additional countries for comparison
□ Implement time series forecasting (ARIMA, Prophet)
□ Add more interactive dashboard features
Medium-term Goals
☑ Deploy dashboard to Streamlit Cloud ✅
□ Create a REST API for data access
□ Build a mobile-friendly version
□ Add machine learning models
Long-term Vision
□ Comprehensive African countries analysis
□ Real-time data updates
□ Policy simulation tools
□ Research paper publication
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit changes: git commit -m 'Add amazing feature'

Push to branch: git push origin feature/amazing-feature

Open a Pull Request

Development Guidelines
Use PEP 8 style guide

Write docstrings for all functions

Add type hints where possible

Keep dependencies minimal

📄 License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

text
MIT License

Copyright (c) 2026 Mxolisi Maseko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
📞 Contact
<div align="center">
Mxolisi Maseko
📧 ismailMxolisi78@gmail.com
🔗 LinkedIn
💻 GitHub
🌐 Portfolio

</div>
🙏 Acknowledgments
World Bank - For providing open data

ILO - For unemployment statistics

UNESCO - For education statistics

Streamlit - For the amazing dashboard framework

Open Source Community - For all the tools used

📚 References
World Bank. (2024). World Development Indicators. https://data.worldbank.org/

ILO. (2024). ILO Modelled Estimates and Projections. https://ilostat.ilo.org/

UNESCO. (2024). UNESCO Institute for Statistics. http://uis.unesco.org/

<div align="center">
⭐ If you found this project useful, please give it a star!
Built with ❤️ for the data science community

Last Updated: August 2026

</div> ```