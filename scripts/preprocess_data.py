#!/usr/bin/env python3
"""
Data preprocessing script for cleaning and preparing bank review data.

This script handles:
- Loading raw scraped data
- Removing duplicates
- Handling missing values
- Date normalization
- Data validation
- Saving cleaned data

Author: Data Analytics Team
Date: 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Class to preprocess bank review data"""
    
    def __init__(self, input_file='../data/all_reviews_raw.csv'):
        self.input_file = input_file
        self.df = None
        
    def load_data(self):
        """Load raw data from CSV file"""
        try:
            logger.info(f"Loading data from {self.input_file}")
            self.df = pd.read_csv(self.input_file)
            logger.info(f"Loaded {len(self.df)} reviews")
            
            # Display basic info
            logger.info(f"Columns: {list(self.df.columns)}")
            logger.info(f"Shape: {self.df.shape}")
            
            return True
        except FileNotFoundError:
            logger.error(f"File {self.input_file} not found!")
            return False
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def remove_duplicates(self):
        """Remove duplicate reviews"""
        logger.info("Removing duplicates...")
        
        initial_count = len(self.df)
        
        # Remove duplicates based on review content and bank
        self.df = self.df.drop_duplicates(subset=['review', 'bank'], keep='first')
        
        final_count = len(self.df)
        removed_count = initial_count - final_count
        
        logger.info(f"Removed {removed_count} duplicate reviews")
        logger.info(f"Remaining reviews: {final_count}")
    
    def handle_missing_data(self):
        """Handle missing values in the dataset"""
        logger.info("Handling missing data...")
        
        # Check for missing values
        missing_summary = self.df.isnull().sum()
        logger.info("Missing values per column:")
        for col, count in missing_summary.items():
            if count > 0:
                logger.info(f"  {col}: {count} missing values")
        
        # Remove rows with missing review content (critical field)
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['review'])
        final_count = len(self.df)
        
        if initial_count != final_count:
            logger.info(f"Removed {initial_count - final_count} rows with missing review content")
        
        # Handle missing ratings (fill with median rating for that bank)
        if self.df['rating'].isnull().sum() > 0:
            logger.info("Filling missing ratings with bank median...")
            self.df['rating'] = self.df.groupby('bank')['rating'].transform(
                lambda x: x.fillna(x.median())
            )
        
        # Handle missing dates (fill with a default date or remove)
        if self.df['date'].isnull().sum() > 0:
            logger.info("Handling missing dates...")
            # Remove rows with missing dates as they're important for analysis
            self.df = self.df.dropna(subset=['date'])
    
    def clean_text_data(self):
        """Clean and standardize text data"""
        logger.info("Cleaning text data...")
        
        # Clean review text
        def clean_review_text(text):
            if pd.isna(text):
                return ""
            
            # Convert to string
            text = str(text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Remove very short reviews (less than 10 characters)
            if len(text) < 10:
                return None
            
            return text
        
        # Apply text cleaning
        self.df['review'] = self.df['review'].apply(clean_review_text)
        
        # Remove rows with empty reviews after cleaning
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['review'])
        final_count = len(self.df)
        
        if initial_count != final_count:
            logger.info(f"Removed {initial_count - final_count} rows with very short reviews")
    
    def normalize_dates(self):
        """Normalize date formats"""
        logger.info("Normalizing dates...")
        
        def parse_date(date_str):
            """Parse various date formats"""
            if pd.isna(date_str):
                return None
            
            try:
                # Try parsing as datetime
                if isinstance(date_str, str):
                    # Handle various date formats
                    parsed_date = pd.to_datetime(date_str)
                else:
                    parsed_date = pd.to_datetime(date_str)
                
                # Format as YYYY-MM-DD
                return parsed_date.strftime('%Y-%m-%d')
            except:
                logger.warning(f"Could not parse date: {date_str}")
                return None
        
        # Apply date normalization
        self.df['date'] = self.df['date'].apply(parse_date)
        
        # Remove rows with unparseable dates
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['date'])
        final_count = len(self.df)
        
        if initial_count != final_count:
            logger.info(f"Removed {initial_count - final_count} rows with invalid dates")
    
    def validate_data(self):
        """Validate data quality and constraints"""
        logger.info("Validating data...")
        
        # Check rating range (should be 1-5)
        invalid_ratings = self.df[(self.df['rating'] < 1) | (self.df['rating'] > 5)]
        if len(invalid_ratings) > 0:
            logger.warning(f"Found {len(invalid_ratings)} reviews with invalid ratings")
            # Remove invalid ratings
            self.df = self.df[(self.df['rating'] >= 1) & (self.df['rating'] <= 5)]
        
        # Check for required columns
        required_columns = ['review', 'rating', 'date', 'bank', 'source']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        # Check minimum data requirements
        min_reviews_per_bank = 100  # Minimum acceptable
        bank_counts = self.df['bank'].value_counts()
        
        logger.info("Reviews per bank after preprocessing:")
        for bank, count in bank_counts.items():
            logger.info(f"  {bank}: {count} reviews")
            if count < min_reviews_per_bank:
                logger.warning(f"  Warning: {bank} has fewer than {min_reviews_per_bank} reviews")
        
        return True
    
    def add_metadata(self):
        """Add useful metadata columns"""
        logger.info("Adding metadata...")
        
        # Add review length
        self.df['review_length'] = self.df['review'].str.len()
        
        # Add word count
        self.df['word_count'] = self.df['review'].str.split().str.len()
        
        # Add processing timestamp
        self.df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def save_cleaned_data(self, output_file='../data/cleaned_reviews.csv'):
        """Save cleaned data to CSV"""
        logger.info(f"Saving cleaned data to {output_file}")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Select final columns in the required order
        final_columns = ['review', 'rating', 'date', 'bank', 'source', 
                        'review_length', 'word_count', 'processed_at']
        
        # Only include columns that exist
        available_columns = [col for col in final_columns if col in self.df.columns]
        final_df = self.df[available_columns]
        
        # Save to CSV
        final_df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(final_df)} cleaned reviews")
        
        return output_file
    
    def generate_summary_report(self):
        """Generate a summary report of the preprocessing"""
        logger.info("\n" + "="*60)
        logger.info("PREPROCESSING SUMMARY REPORT")
        logger.info("="*60)
        
        # Basic statistics
        logger.info(f"Total reviews after preprocessing: {len(self.df)}")
        logger.info(f"Date range: {self.df['date'].min()} to {self.df['date'].max()}")
        
        # Bank distribution
        logger.info("\nReviews per bank:")
        bank_counts = self.df['bank'].value_counts()
        for bank, count in bank_counts.items():
            percentage = (count / len(self.df)) * 100
            logger.info(f"  {bank}: {count} reviews ({percentage:.1f}%)")
        
        # Rating distribution
        logger.info("\nRating distribution:")
        rating_counts = self.df['rating'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            percentage = (count / len(self.df)) * 100
            logger.info(f"  {rating} stars: {count} reviews ({percentage:.1f}%)")
        
        # Text statistics
        logger.info(f"\nText statistics:")
        logger.info(f"  Average review length: {self.df['review_length'].mean():.1f} characters")
        logger.info(f"  Average word count: {self.df['word_count'].mean():.1f} words")
        logger.info(f"  Shortest review: {self.df['review_length'].min()} characters")
        logger.info(f"  Longest review: {self.df['review_length'].max()} characters")
        
        # Data quality metrics
        missing_data = self.df.isnull().sum().sum()
        data_quality_score = ((len(self.df) * len(self.df.columns) - missing_data) / 
                             (len(self.df) * len(self.df.columns))) * 100
        logger.info(f"\nData quality score: {data_quality_score:.2f}%")
        
        logger.info("\nPreprocessing completed successfully!")
    
    def process_all(self):
        """Run the complete preprocessing pipeline"""
        logger.info("Starting data preprocessing pipeline...")
        
        # Load data
        if not self.load_data():
            return False
        
        # Run preprocessing steps
        self.remove_duplicates()
        self.handle_missing_data()
        self.clean_text_data()
        self.normalize_dates()
        
        # Validate data
        if not self.validate_data():
            logger.error("Data validation failed!")
            return False
        
        # Add metadata
        self.add_metadata()
        
        # Save cleaned data
        output_file = self.save_cleaned_data()
        
        # Generate summary report
        self.generate_summary_report()
        
        return output_file

def main():
    """Main function to run preprocessing"""
    logger.info("Starting Data Preprocessing")
    logger.info(f"Timestamp: {datetime.now()}")
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Run preprocessing
    result = preprocessor.process_all()
    
    if result:
        logger.info(f"Preprocessing completed successfully!")
        logger.info(f"Cleaned data saved to: {result}")
    else:
        logger.error("Preprocessing failed!")

if __name__ == "__main__":
    main() 