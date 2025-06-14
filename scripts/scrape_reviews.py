#!/usr/bin/env python3
"""
Web scraper for collecting mobile banking app reviews from Google Play Store
for Ethiopian banks: CBE, BOA, and Dashen Bank.

Author: Data Analytics Team
Date: 2024
"""

import pandas as pd
from google_play_scraper import app, reviews_all
import time
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BankReviewScraper:
    """Class to scrape reviews for Ethiopian bank mobile apps"""
    
    def __init__(self):
        # Bank app IDs on Google Play Store (verified from web search)
        self.bank_apps = {
            'CBE': 'com.combanketh.mobilebanking',  # Commercial Bank of Ethiopia
            'BOA': 'com.boa.boaMobileBanking',      # Bank of Abyssinia (BoA Mobile)
            'Dashen': 'com.dashen.dashensuperapp'   # Dashen Bank (SuperApp)
        }
        
        # Create data directory if it doesn't exist
        os.makedirs('../data', exist_ok=True)
        
    def scrape_bank_reviews(self, bank_name, app_id, target_reviews=400):
        """
        Scrape reviews for a specific bank app
        
        Args:
            bank_name (str): Name of the bank
            app_id (str): Google Play Store app ID
            target_reviews (int): Target number of reviews to scrape
            
        Returns:
            pd.DataFrame: DataFrame containing scraped reviews
        """
        logger.info(f"Starting to scrape reviews for {bank_name}...")
        
        try:
            # Get app information
            app_info = app(app_id)
            logger.info(f"App: {app_info['title']} - Rating: {app_info['score']}")
            
            # Scrape all available reviews
            reviews = reviews_all(
                app_id,
                sleep_milliseconds=1000,  # Be respectful to the API
                lang='en',
                country='et'  # Ethiopia
            )
            
            logger.info(f"Successfully scraped {len(reviews)} reviews for {bank_name}")
            
            # Convert to DataFrame
            df = pd.DataFrame(reviews)
            
            # Add bank information
            df['bank'] = bank_name
            df['app_name'] = app_info['title']
            df['source'] = 'Google Play Store'
            
            # Select and rename columns to match requirements
            df = df.rename(columns={
                'content': 'review',
                'score': 'rating',
                'at': 'date'
            })
            
            # Select required columns
            required_columns = ['review', 'rating', 'date', 'bank', 'source']
            df = df[required_columns + ['app_name']]  # Keep app_name for reference
            
            # Limit to target number of reviews if we have more
            if len(df) > target_reviews:
                df = df.head(target_reviews)
                logger.info(f"Limited to {target_reviews} reviews for {bank_name}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error scraping reviews for {bank_name}: {str(e)}")
            return pd.DataFrame()
    
    def scrape_all_banks(self, target_per_bank=400):
        """
        Scrape reviews for all banks
        
        Args:
            target_per_bank (int): Target number of reviews per bank
            
        Returns:
            pd.DataFrame: Combined DataFrame with all reviews
        """
        all_reviews = []
        
        for bank_name, app_id in self.bank_apps.items():
            logger.info(f"\n{'='*50}")
            logger.info(f"Scraping {bank_name}")
            logger.info(f"{'='*50}")
            
            # Scrape reviews for this bank
            bank_reviews = self.scrape_bank_reviews(bank_name, app_id, target_per_bank)
            
            if not bank_reviews.empty:
                all_reviews.append(bank_reviews)
                
                # Save individual bank data
                filename = f"../data/{bank_name.lower()}_reviews_raw.csv"
                bank_reviews.to_csv(filename, index=False)
                logger.info(f"Saved {len(bank_reviews)} reviews to {filename}")
            
            # Be respectful - wait between banks
            time.sleep(2)
        
        # Combine all reviews
        if all_reviews:
            combined_df = pd.concat(all_reviews, ignore_index=True)
            logger.info(f"\nTotal reviews scraped: {len(combined_df)}")
            
            # Save combined raw data
            combined_df.to_csv('../data/all_reviews_raw.csv', index=False)
            logger.info("Saved combined raw data to ../data/all_reviews_raw.csv")
            
            return combined_df
        else:
            logger.error("No reviews were successfully scraped!")
            return pd.DataFrame()

def main():
    """Main function to run the scraper"""
    logger.info("Starting Bank Review Scraper")
    logger.info(f"Timestamp: {datetime.now()}")
    
    # Initialize scraper
    scraper = BankReviewScraper()
    
    # Scrape all reviews
    all_reviews = scraper.scrape_all_banks(target_per_bank=400)
    
    if not all_reviews.empty:
        # Display summary statistics
        logger.info("\n" + "="*60)
        logger.info("SCRAPING SUMMARY")
        logger.info("="*60)
        
        for bank in all_reviews['bank'].unique():
            bank_count = len(all_reviews[all_reviews['bank'] == bank])
            logger.info(f"{bank}: {bank_count} reviews")
        
        logger.info(f"Total: {len(all_reviews)} reviews")
        logger.info(f"Date range: {all_reviews['date'].min()} to {all_reviews['date'].max()}")
        
        # Show rating distribution
        logger.info("\nRating Distribution:")
        rating_dist = all_reviews['rating'].value_counts().sort_index()
        for rating, count in rating_dist.items():
            logger.info(f"  {rating} stars: {count} reviews")
        
        logger.info("\nScraping completed successfully!")
    else:
        logger.error("Scraping failed - no data collected")

if __name__ == "__main__":
    main() 