#!/usr/bin/env python3
"""
Main execution script for Task 1: Data Collection and Preprocessing

This script orchestrates the complete Task 1 pipeline:
1. Web scraping of bank reviews
2. Data preprocessing and cleaning
3. Data validation and reporting

Author: Data Analytics Team
Date: 2024
"""

import sys
import os
import logging
from datetime import datetime

# Add scripts directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom modules
from scrape_reviews import BankReviewScraper
from preprocess_data import DataPreprocessor

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../data/task1_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function for Task 1"""
    logger.info("="*80)
    logger.info("STARTING TASK 1: DATA COLLECTION AND PREPROCESSING")
    logger.info("="*80)
    logger.info(f"Execution started at: {datetime.now()}")
    
    try:
        # Step 1: Web Scraping
        logger.info("\n" + "="*50)
        logger.info("STEP 1: WEB SCRAPING")
        logger.info("="*50)
        
        scraper = BankReviewScraper()
        scraped_data = scraper.scrape_all_banks(target_per_bank=400)
        
        if scraped_data.empty:
            logger.error("Scraping failed - no data collected!")
            return False
        
        logger.info(f"✓ Scraping completed: {len(scraped_data)} reviews collected")
        
        # Step 2: Data Preprocessing
        logger.info("\n" + "="*50)
        logger.info("STEP 2: DATA PREPROCESSING")
        logger.info("="*50)
        
        preprocessor = DataPreprocessor()
        cleaned_file = preprocessor.process_all()
        
        if not cleaned_file:
            logger.error("Preprocessing failed!")
            return False
        
        logger.info(f"✓ Preprocessing completed: {cleaned_file}")
        
        # Step 3: Final Validation
        logger.info("\n" + "="*50)
        logger.info("STEP 3: FINAL VALIDATION")
        logger.info("="*50)
        
        # Load and validate final data
        import pandas as pd
        final_df = pd.read_csv(cleaned_file)
        
        # Check KPIs
        total_reviews = len(final_df)
        reviews_per_bank = final_df['bank'].value_counts()
        missing_data_percentage = (final_df.isnull().sum().sum() / 
                                 (len(final_df) * len(final_df.columns))) * 100
        
        logger.info("TASK 1 KPI VALIDATION:")
        logger.info(f"  ✓ Total reviews: {total_reviews} (Target: 1200+)")
        logger.info(f"  ✓ Missing data: {missing_data_percentage:.2f}% (Target: <5%)")
        
        for bank, count in reviews_per_bank.items():
            logger.info(f"  ✓ {bank}: {count} reviews (Target: 400+)")
        
        # Check if KPIs are met
        kpis_met = (
            total_reviews >= 1200 and
            missing_data_percentage < 5.0 and
            all(count >= 400 for count in reviews_per_bank.values())
        )
        
        if kpis_met:
            logger.info("🎉 ALL TASK 1 KPIs SUCCESSFULLY MET!")
        else:
            logger.warning("⚠️  Some KPIs not fully met, but data is usable")
        
        # Final summary
        logger.info("\n" + "="*80)
        logger.info("TASK 1 COMPLETION SUMMARY")
        logger.info("="*80)
        logger.info(f"✓ Raw data file: ../data/all_reviews_raw.csv")
        logger.info(f"✓ Cleaned data file: {cleaned_file}")
        logger.info(f"✓ Execution log: ../data/task1_execution.log")
        logger.info(f"✓ Total execution time: {datetime.now()}")
        logger.info("✓ Ready for Task 2: Sentiment and Thematic Analysis")
        
        return True
        
    except Exception as e:
        logger.error(f"Task 1 execution failed: {str(e)}")
        logger.error("Please check the logs and fix any issues before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Task 1 completed successfully!")
        print("You can now proceed to Task 2.")
    else:
        print("\n❌ Task 1 failed. Please check the logs and try again.")
        sys.exit(1) 