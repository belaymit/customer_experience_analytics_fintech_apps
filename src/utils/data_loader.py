"""
Data loading and basic preprocessing utilities for sentiment analysis.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

class DataLoader:
    """Handles data loading and basic preprocessing for sentiment analysis."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def load_reviews_data(self, file_path: str) -> pd.DataFrame:
        """
        Load reviews data from CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded reviews data
        """
        try:
            df = pd.read_csv(file_path)
            self.logger.info(f"Loaded {len(df)} reviews from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading data from {file_path}: {str(e)}")
            raise
    
    def basic_data_info(self, df: pd.DataFrame) -> dict:
        """
        Get basic information about the dataset.
        
        Args:
            df (pd.DataFrame): Reviews dataframe
            
        Returns:
            dict: Basic statistics about the data
        """
        info = {
            'total_reviews': len(df),
            'columns': list(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict(),
            'unique_banks': df['bank'].unique().tolist() if 'bank' in df.columns else [],
            'date_range': {
                'min': df['date'].min() if 'date' in df.columns else None,
                'max': df['date'].max() if 'date' in df.columns else None
            } if 'date' in df.columns else None,
            'rating_stats': df['rating'].describe().to_dict() if 'rating' in df.columns else None
        }
        return info
    
    def clean_text_data(self, df: pd.DataFrame, text_column: str = 'review') -> pd.DataFrame:
        """
        Basic text cleaning operations.
        
        Args:
            df (pd.DataFrame): Reviews dataframe
            text_column (str): Name of the text column to clean
            
        Returns:
            pd.DataFrame: Dataframe with cleaned text
        """
        df_clean = df.copy()
        
        # Remove null values
        df_clean = df_clean.dropna(subset=[text_column])
        
        # Basic text cleaning
        df_clean[text_column] = df_clean[text_column].astype(str)
        df_clean[f'{text_column}_length'] = df_clean[text_column].str.len()
        
        # Remove very short reviews (less than 10 characters)
        df_clean = df_clean[df_clean[f'{text_column}_length'] >= 10]
        
        self.logger.info(f"Cleaned data: {len(df_clean)} reviews remaining")
        return df_clean
    
    def get_bank_distribution(self, df: pd.DataFrame) -> pd.Series:
        """
        Get distribution of reviews by bank.
        
        Args:
            df (pd.DataFrame): Reviews dataframe
            
        Returns:
            pd.Series: Count of reviews per bank
        """
        if 'bank' in df.columns:
            return df['bank'].value_counts()
        else:
            return pd.Series()
    
    def get_rating_distribution(self, df: pd.DataFrame) -> pd.Series:
        """
        Get distribution of ratings.
        
        Args:
            df (pd.DataFrame): Reviews dataframe
            
        Returns:
            pd.Series: Count of reviews per rating
        """
        if 'rating' in df.columns:
            return df['rating'].value_counts().sort_index()
        else:
            return pd.Series() 