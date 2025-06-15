# Task 2: Modular Sentiment and Thematic Analysis

This directory contains a modular implementation of sentiment and thematic analysis for Ethiopian banking app reviews.

## 🏗️ Architecture Overview

The code is organized into modular components for better maintainability, reusability, and testing:

```
src/
├── utils/
│   ├── data_loader.py          # Data loading and basic preprocessing
│   └── text_preprocessor.py    # Advanced text preprocessing
├── sentiment_analysis/
│   ├── sentiment_analyzer.py   # DistilBERT + TextBlob sentiment analysis
│   └── theme_analyzer.py       # Thematic analysis with predefined categories
└── visualization/
    └── plots.py                # Comprehensive visualization utilities
```

## 📊 Components

### 1. Data Loader (`src/utils/data_loader.py`)
- **Purpose**: Handle data loading and basic preprocessing
- **Key Features**:
  - Load CSV data with error handling
  - Basic data information and statistics
  - Data cleaning and validation
  - Bank and rating distribution analysis

### 2. Text Preprocessor (`src/utils/text_preprocessor.py`)
- **Purpose**: Advanced text cleaning and preprocessing
- **Key Features**:
  - Text normalization and cleaning
  - Tokenization with NLTK
  - Stopword removal
  - Lemmatization
  - Keyword extraction

### 3. Sentiment Analyzer (`src/sentiment_analysis/sentiment_analyzer.py`)
- **Purpose**: Perform sentiment analysis using multiple approaches
- **Key Features**:
  - DistilBERT model for advanced sentiment analysis
  - TextBlob fallback for reliability
  - Batch processing capabilities
  - Confidence scoring
  - Summary statistics generation

### 4. Theme Analyzer (`src/sentiment_analysis/theme_analyzer.py`)
- **Purpose**: Identify themes in banking app reviews
- **Key Features**:
  - 8 predefined theme categories:
    - UI/UX Issues
    - Performance Issues
    - Transaction Issues
    - Security Features
    - Network Connectivity
    - Customer Support
    - Feature Requests
    - Account Access
  - TF-IDF keyword extraction
  - Theme-sentiment correlation analysis
  - Bank-wise theme comparison

### 5. Visualization (`src/visualization/plots.py`)
- **Purpose**: Create comprehensive visualizations
- **Key Features**:
  - Sentiment distribution plots
  - Bank comparison charts
  - Theme analysis visualizations
  - Correlation heatmaps
  - Word clouds
  - Comprehensive dashboard

## 🚀 Usage

### Option 1: Interactive Jupyter Notebookr
```bash
jupyter notebook task2_sentiment_analysis_interactive.ipynb
```

This notebook provides:
- Step-by-step analysis with explanations
- Data exploration with `df.head()` at each step
- Interactive visualizations
- Comprehensive heatmaps and matrices
- Real-time insights generation

### Option 2: Command Line Script
```bash
python task2_main.py
```

This script runs the complete pipeline and saves results automatically.

### Option 3: Import as Modules
```python
from src.utils.data_loader import DataLoader
from src.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from src.sentiment_analysis.theme_analyzer import ThemeAnalyzer
from src.visualization.plots import SentimentVisualizer

# Use components individually
data_loader = DataLoader()
df = data_loader.load_reviews_data('data/cleaned_reviews.csv')

sentiment_analyzer = SentimentAnalyzer()
df_sentiment = sentiment_analyzer.analyze_dataframe(df)
```

## 📈 Key Features

### Modular Design Benefits
- **Separation of Concerns**: Each module has a specific responsibility
- **Reusability**: Components can be used independently
- **Testability**: Easy to unit test individual components
- **Maintainability**: Changes in one module don't affect others
- **Extensibility**: Easy to add new features or analysis methods

### Interactive Analysis
- **Step-by-step exploration**: See data at each processing stage
- **Visual feedback**: Comprehensive charts and heatmaps
- **Real-time insights**: Generate actionable recommendations
- **Data inspection**: `df.head()`, `df.info()`, and detailed statistics

### Comprehensive Visualizations
- Sentiment distribution (pie charts, bar charts)
- Bank comparison (stacked bars, heatmaps)
- Theme analysis (distribution, correlation matrices)
- Rating Correlation: Box plots and heatmaps
- Confidence Analysis: Histograms and distributions
- Comprehensive Dashboard: All-in-one overview

## 🎯 Analysis Pipeline

1. **Data Loading**: Load and validate review data
2. **Text Preprocessing**: Clean and prepare text for analysis
3. **Sentiment Analysis**: Apply DistilBERT + TextBlob models
4. **Theme Analysis**: Identify key themes using keyword matching
5. **Visualization**: Create comprehensive charts and heatmaps
6. **Bank Comparison**: Compare performance across banks
7. **Insights Generation**: Generate actionable recommendations
8. **Results Export**: Save analysis results and insights

## 📊 Output Files

The analysis generates several output files:
- `task2_sentiment_thematic_analysis_interactive_[timestamp].csv` - Complete analysis results
- `insights_interactive_[timestamp].json` - Detailed insights and recommendations
- `bank_comparison_[timestamp].csv` - Bank performance comparison
- Various visualization plots (if saved)

## 🔧 Dependencies

All required packages are listed in `requirements.txt`:
- `transformers` - DistilBERT model
- `torch` - PyTorch backend
- `nltk` - Text preprocessing
- `textblob` - Sentiment analysis fallback
- `scikit-learn` - TF-IDF vectorization
- `matplotlib` & `seaborn` - Visualizations
- `wordcloud` - Word cloud generation
- `pandas` & `numpy` - Data manipulation

## 🎨 Visualization Examples

The modular approach provides rich visualizations:
- **Sentiment Distribution**: Pie charts and bar plots
- **Bank Comparison**: Stacked bars and heatmaps
- **Theme Analysis**: Distribution plots and correlation matrices
- **Rating Correlation**: Box plots and heatmaps
- **Confidence Analysis**: Histograms and distributions
- **Comprehensive Dashboard**: All-in-one overview

## 💡 Key Insights Generated

The analysis provides actionable insights:
- Overall sentiment distribution across all reviews
- Bank performance ranking and comparison
- Most problematic themes (high negative sentiment)
- Success factors (themes with positive sentiment)
- Specific recommendations for each bank
- Theme-sentiment correlation patterns

## 🧪 Testing

The modular design makes testing straightforward:
```python
# Test individual components
from src.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
result = analyzer.analyze_sentiment_distilbert("Great app!")
assert result['sentiment'] == 'positive'
```

## 🔄 Extensibility

Easy to extend with new features:
- Add new theme categories in `ThemeAnalyzer`
- Implement new sentiment models in `SentimentAnalyzer`
- Create new visualization types in `SentimentVisualizer`
- Add new data sources in `DataLoader`

This modular approach provides a robust, maintainable, and extensible framework for sentiment and thematic analysis of banking app reviews. 