"""
Task 2: Modular Sentiment and Thematic Analysis
Main script demonstrating the modular approach for analyzing Ethiopian banking app reviews.
"""

import sys
import logging
from datetime import datetime

# Add src to path
sys.path.append('src')

# Import modular components
from utils.data_loader import DataLoader
from utils.text_preprocessor import TextPreprocessor
from sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from sentiment_analysis.theme_analyzer import ThemeAnalyzer
from visualization.plots import SentimentVisualizer

def main():
    """Main function to run the complete analysis pipeline."""
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    print("🚀 Starting Task 2: Sentiment and Thematic Analysis")
    print("="*60)
    print(f"Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Load Data
        print("\n📊 Step 1: Loading Data...")
        data_loader = DataLoader()
        df = data_loader.load_reviews_data('data/cleaned_reviews.csv')
        df_clean = data_loader.clean_text_data(df, 'review')
        print(f"✅ Loaded and cleaned {len(df_clean):,} reviews")
        
        # 2. Initialize Components
        print("\n🔧 Step 2: Initializing Analysis Components...")
        text_preprocessor = TextPreprocessor()
        sentiment_analyzer = SentimentAnalyzer()
        theme_analyzer = ThemeAnalyzer()
        visualizer = SentimentVisualizer()
        print("✅ All components initialized successfully")
        
        # 3. Sentiment Analysis
        print("\n🤖 Step 3: Performing Sentiment Analysis...")
        df_sentiment = sentiment_analyzer.analyze_dataframe(df_clean, 'review')
        sentiment_summary = sentiment_analyzer.get_sentiment_summary(df_sentiment)
        print(f"✅ Sentiment analysis completed")
        print(f"   Positive: {sentiment_summary['sentiment_percentages']['positive']:.1f}%")
        print(f"   Negative: {sentiment_summary['sentiment_percentages']['negative']:.1f}%")
        print(f"   Neutral: {sentiment_summary['sentiment_percentages']['neutral']:.1f}%")
        
        # 4. Theme Analysis
        print("\n🔍 Step 4: Performing Theme Analysis...")
        df_complete = theme_analyzer.analyze_dataframe(df_sentiment, 'review')
        theme_summary = theme_analyzer.get_theme_summary(df_complete)
        print(f"✅ Theme analysis completed")
        print(f"   Reviews with themes: {theme_summary['reviews_with_themes']:,}")
        print(f"   Average themes per review: {theme_summary['average_themes_per_review']:.2f}")
        
        # 5. Generate Insights
        print("\n💡 Step 5: Generating Insights...")
        theme_sentiment_corr = theme_analyzer.get_theme_sentiment_correlation(df_complete)
        
        # Bank comparison
        bank_analysis = {}
        for bank in df_complete['bank'].unique():
            bank_df = df_complete[df_complete['bank'] == bank]
            bank_summary = sentiment_analyzer.get_sentiment_summary(bank_df)
            bank_analysis[bank] = {
                'total_reviews': len(bank_df),
                'avg_rating': bank_df['rating'].mean(),
                'positive_pct': bank_summary['sentiment_percentages']['positive'],
                'negative_pct': bank_summary['sentiment_percentages']['negative']
            }
        
        print("✅ Insights generated successfully")
        
        # 6. Save Results
        print("\n💾 Step 6: Saving Results...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save main results
        output_file = f'task2_modular_analysis_{timestamp}.csv'
        df_complete.to_csv(output_file, index=False)
        
        # Save insights
        import json
        insights = {
            'timestamp': timestamp,
            'total_reviews': len(df_complete),
            'sentiment_summary': sentiment_summary,
            'theme_summary': theme_summary,
            'bank_analysis': bank_analysis,
            'theme_sentiment_correlation': theme_sentiment_corr
        }
        
        insights_file = f'task2_insights_{timestamp}.json'
        with open(insights_file, 'w') as f:
            json.dump(insights, f, indent=2, default=str)
        
        print(f"✅ Results saved:")
        print(f"   📄 Analysis data: {output_file}")
        print(f"   📊 Insights: {insights_file}")
        
        # 7. Summary
        print(f"\n🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"📊 Total Reviews: {len(df_complete):,}")
        print(f"🏦 Banks Analyzed: {', '.join(df_complete['bank'].unique())}")
        print(f"🎯 Overall Sentiment: {sentiment_summary['sentiment_percentages']['positive']:.1f}% positive")
        print(f"🔍 Top Theme: {theme_summary['most_common_themes'][0][0].replace('_', ' ')}")
        print(f"⏱️  Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return df_complete, insights
        
    except Exception as e:
        logger.error(f"Error in analysis pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    df_results, analysis_insights = main() 