# Customer Experience Analytics for Fintech Apps

This repository contains the analysis of customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)  
- Dashen Bank

## Project Overview

The project simulates the role of a Data Analyst at Omega Consultancy, a firm advising banks on improving their mobile apps to enhance customer retention and satisfaction.

### Business Objectives

- Scrape user reviews from the Google Play Store
- Analyze sentiment (positive/negative/neutral) and extract themes
- Identify satisfaction drivers and pain points
- Store cleaned review data in a database
- Deliver actionable recommendations with visualizations

## Repository Structure

```
customer_experience_analytics_fintech_apps/
├── data/                    # Data files (CSV, processed datasets)
│   ├── all_reviews_raw.csv     # Raw scraped data
│   ├── cleaned_reviews.csv     # Preprocessed data
│   └── task1_execution.log     # Task 1 execution logs
├── scripts/                 # Python scripts for analysis
│   ├── scrape_reviews.py       # Web scraping script
│   ├── preprocess_data.py      # Data preprocessing script
│   └── run_task1.py           # Task 1 main execution script
├── notebooks/              # Jupyter notebooks for exploration
├── reports/                # Analysis reports and visualizations
├── database/               # Database schema and scripts
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd customer_experience_analytics_fintech_apps
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Task 1: Data Collection and Preprocessing ✅

### Overview
Task 1 focuses on collecting and preprocessing mobile banking app reviews from the Google Play Store.

### Methodology

#### 1. Web Scraping
- **Tool**: `google-play-scraper` library
- **Target**: 400+ reviews per bank (1,200+ total)
- **Banks**: CBE, BOA, Dashen Bank
- **Data Points**: Review text, rating, date, bank name, source

#### 2. Data Preprocessing
- **Duplicate Removal**: Based on review content and bank
- **Missing Data Handling**: Remove critical missing fields, impute others
- **Text Cleaning**: Standardize whitespace, remove very short reviews
- **Date Normalization**: Convert to YYYY-MM-DD format
- **Data Validation**: Ensure rating ranges (1-5), required columns present

#### 3. Quality Assurance
- **Data Quality Score**: >95% completeness
- **Review Distribution**: Balanced across banks
- **Text Statistics**: Average length, word count analysis

### Execution

To run Task 1 complete pipeline:

```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to scripts directory
cd scripts

# Run the complete Task 1 pipeline
python run_task1.py
```

### Individual Script Usage

```bash
# Run only web scraping
python scrape_reviews.py

# Run only preprocessing (requires raw data)
python preprocess_data.py
```

### Output Files

- `data/all_reviews_raw.csv`: Raw scraped data
- `data/cleaned_reviews.csv`: Preprocessed, analysis-ready data
- `data/task1_execution.log`: Detailed execution logs
- Individual bank files: `data/{bank}_reviews_raw.csv`

### MongoDB Cloud Storage

Store your data in MongoDB Atlas for advanced analysis:

```bash
# Upload to MongoDB Atlas
cd scripts
python mongodb_storage.py

# Run analysis queries
python mongodb_queries.py
```

See `MONGODB_SETUP.md` for detailed setup instructions.

### KPIs Achieved

- ✅ **1,200+ reviews** collected across three banks
- ✅ **<5% missing data** after preprocessing
- ✅ **Clean CSV dataset** with required columns
- ✅ **Organized Git workflow** with meaningful commits
- ✅ **Comprehensive documentation** and logging

## Tasks Overview

### Task 1: Data Collection and Preprocessing ✅
- Web scraping from Google Play Store
- Data cleaning and preprocessing
- Git workflow management

### Task 2: Sentiment and Thematic Analysis (Next)
- Sentiment analysis using NLP models
- Keyword extraction and theme identification
- Data pipeline development

### Task 3: Database Storage
- Oracle database setup and schema design
- Data insertion and management
- SQL query development

### Task 4: Insights and Recommendations
- Data visualization and analysis
- Business insights extraction
- Report generation

## Key Performance Indicators (KPIs)

- **Data Quality**: 1,200+ clean reviews with <5% errors ✅
- **Insights**: 3+ drivers/pain points per bank
- **Visualizations**: Stakeholder-friendly charts and graphs
- **Code Quality**: Well-documented, modular code with version control ✅

## Technologies Used

- **Web Scraping**: google-play-scraper
- **Data Processing**: pandas, numpy
- **NLP**: transformers, spaCy, VADER
- **Database**: Oracle XE
- **Visualization**: matplotlib, seaborn
- **Version Control**: Git/GitHub

## Contributing

1. Create a feature branch from main
2. Make your changes
3. Commit with meaningful messages
4. Create a pull request

## License

This project is licensed under the MIT License - see the [MIT.md](MIT.md) file for details.

## Contact

For questions or support, please contact the development team.

---

*This project is part of the KAIM (Kigali AI & ML) program focusing on practical data analytics applications in the fintech sector.*
