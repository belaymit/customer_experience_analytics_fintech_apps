"""
Theme analysis module for identifying themes in banking app reviews.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from sklearn.feature_extraction.text import TfidfVectorizer

class ThemeAnalyzer:
    """Handles thematic analysis of banking app reviews."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.theme_keywords = {
            'UI_UX_Issues': [
                'interface', 'design', 'layout', 'navigation', 'menu', 'button', 'screen',
                'user experience', 'ux', 'ui', 'confusing', 'difficult', 'hard to use',
                'complicated', 'intuitive', 'easy', 'simple', 'clean', 'messy'
            ],
            'Performance_Issues': [
                'slow', 'fast', 'speed', 'loading', 'lag', 'freeze', 'crash', 'hang',
                'performance', 'quick', 'responsive', 'unresponsive', 'timeout',
                'delay', 'wait', 'stuck', 'frozen'
            ],
            'Transaction_Issues': [
                'transaction', 'transfer', 'payment', 'send money', 'receive money',
                'balance', 'account', 'deposit', 'withdrawal', 'failed transaction',
                'pending', 'successful', 'error', 'declined', 'approved'
            ],
            'Security_Features': [
                'security', 'safe', 'secure', 'password', 'pin', 'fingerprint',
                'biometric', 'authentication', 'login', 'logout', 'privacy',
                'protection', 'fraud', 'hack', 'breach', 'trust'
            ],
            'Network_Connectivity': [
                'network', 'internet', 'connection', 'offline', 'online',
                'connectivity', 'signal', 'wifi', 'data', 'mobile data',
                'server', 'down', 'unavailable', 'maintenance'
            ],
            'Customer_Support': [
                'support', 'help', 'customer service', 'assistance', 'contact',
                'call center', 'helpdesk', 'response', 'staff', 'representative',
                'service', 'helpful', 'unhelpful', 'rude', 'polite'
            ],
            'Feature_Requests': [
                'feature', 'add', 'include', 'wish', 'want', 'need', 'missing',
                'should have', 'would like', 'suggestion', 'improvement',
                'update', 'upgrade', 'new feature', 'functionality'
            ],
            'Account_Access': [
                'login', 'access', 'account', 'username', 'password', 'forgot',
                'locked', 'blocked', 'suspended', 'activate', 'deactivate',
                'register', 'signup', 'sign up', 'verification'
            ]
        }
        
        self.tfidf_vectorizer = None
        
    def extract_keywords_tfidf(self, texts: List[str], max_features: int = 100) -> List[str]:
        """
        Extract keywords using TF-IDF.
        
        Args:
            texts (List[str]): List of texts to analyze
            max_features (int): Maximum number of features to extract
            
        Returns:
            List[str]: List of keywords
        """
        try:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=max_features,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
            
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Sort by score
            keyword_scores = list(zip(feature_names, mean_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [keyword for keyword, score in keyword_scores]
            
        except Exception as e:
            self.logger.error(f"TF-IDF keyword extraction failed: {str(e)}")
            return []
    
    def identify_themes(self, text: str) -> List[str]:
        """
        Identify themes in a single text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[str]: List of identified themes
        """
        if not isinstance(text, str):
            return []
        
        text_lower = text.lower()
        identified_themes = []
        
        for theme, keywords in self.theme_keywords.items():
            theme_score = 0
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    theme_score += 1
            
            # If at least one keyword is found, consider the theme present
            if theme_score > 0:
                identified_themes.append(theme)
        
        return identified_themes
    
    def analyze_themes_batch(self, texts: List[str]) -> List[List[str]]:
        """
        Analyze themes for a batch of texts.
        
        Args:
            texts (List[str]): List of texts to analyze
            
        Returns:
            List[List[str]]: List of theme lists for each text
        """
        results = []
        
        for i, text in enumerate(texts):
            if i % 100 == 0:
                self.logger.info(f"Processing theme analysis {i+1}/{len(texts)}")
            
            themes = self.identify_themes(text)
            results.append(themes)
        
        return results
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'review') -> pd.DataFrame:
        """
        Analyze themes for all texts in a dataframe.
        
        Args:
            df (pd.DataFrame): Dataframe containing texts
            text_column (str): Name of the text column
            
        Returns:
            pd.DataFrame: Dataframe with theme analysis results
        """
        df_result = df.copy()
        
        # Analyze themes
        texts = df_result[text_column].astype(str).tolist()
        theme_results = self.analyze_themes_batch(texts)
        
        # Add theme columns
        df_result['themes'] = [', '.join(themes) for themes in theme_results]
        df_result['theme_count'] = [len(themes) for themes in theme_results]
        
        # Add binary columns for each theme
        for theme in self.theme_keywords.keys():
            df_result[f'theme_{theme}'] = [1 if theme in themes else 0 for themes in theme_results]
        
        return df_result
    
    def get_theme_summary(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Get summary statistics of theme analysis.
        
        Args:
            df (pd.DataFrame): Dataframe with theme analysis results
            
        Returns:
            Dict[str, any]: Summary statistics
        """
        if 'themes' not in df.columns:
            return {}
        
        total_reviews = len(df)
        theme_counts = {}
        
        # Count occurrences of each theme
        for theme in self.theme_keywords.keys():
            theme_col = f'theme_{theme}'
            if theme_col in df.columns:
                theme_counts[theme] = df[theme_col].sum()
        
        # Calculate percentages
        theme_percentages = {
            theme: (count / total_reviews) * 100 
            for theme, count in theme_counts.items()
        }
        
        # Get most common themes
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        
        summary = {
            'total_reviews': total_reviews,
            'theme_counts': theme_counts,
            'theme_percentages': theme_percentages,
            'most_common_themes': sorted_themes[:5],
            'average_themes_per_review': df['theme_count'].mean() if 'theme_count' in df.columns else 0,
            'reviews_with_themes': (df['theme_count'] > 0).sum() if 'theme_count' in df.columns else 0
        }
        
        return summary
    
    def get_bank_theme_analysis(self, df: pd.DataFrame) -> Dict[str, Dict[str, any]]:
        """
        Get theme analysis by bank.
        
        Args:
            df (pd.DataFrame): Dataframe with theme analysis results
            
        Returns:
            Dict[str, Dict[str, any]]: Theme analysis by bank
        """
        if 'bank' not in df.columns:
            return {}
        
        bank_analysis = {}
        
        for bank in df['bank'].unique():
            bank_df = df[df['bank'] == bank]
            bank_summary = self.get_theme_summary(bank_df)
            bank_analysis[bank] = bank_summary
        
        return bank_analysis
    
    def extract_theme_keywords(self, df: pd.DataFrame, theme: str, top_n: int = 10) -> List[str]:
        """
        Extract top keywords for a specific theme.
        
        Args:
            df (pd.DataFrame): Dataframe with theme analysis results
            theme (str): Theme to analyze
            top_n (int): Number of top keywords to return
            
        Returns:
            List[str]: List of top keywords for the theme
        """
        theme_col = f'theme_{theme}'
        if theme_col not in df.columns:
            return []
        
        # Get reviews that contain this theme
        theme_reviews = df[df[theme_col] == 1]['review'].astype(str).tolist()
        
        if not theme_reviews:
            return []
        
        # Extract keywords using TF-IDF
        keywords = self.extract_keywords_tfidf(theme_reviews, max_features=top_n)
        
        return keywords[:top_n]
    
    def get_theme_sentiment_correlation(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Analyze correlation between themes and sentiment.
        
        Args:
            df (pd.DataFrame): Dataframe with theme and sentiment analysis results
            
        Returns:
            Dict[str, Dict[str, float]]: Theme-sentiment correlations
        """
        if 'sentiment_sentiment' not in df.columns:
            return {}
        
        correlations = {}
        
        for theme in self.theme_keywords.keys():
            theme_col = f'theme_{theme}'
            if theme_col not in df.columns:
                continue
            
            theme_df = df[df[theme_col] == 1]
            if len(theme_df) == 0:
                continue
            
            sentiment_dist = theme_df['sentiment_sentiment'].value_counts(normalize=True)
            
            correlations[theme] = {
                'positive_ratio': sentiment_dist.get('positive', 0),
                'negative_ratio': sentiment_dist.get('negative', 0),
                'neutral_ratio': sentiment_dist.get('neutral', 0),
                'total_reviews': len(theme_df),
                'avg_confidence': theme_df['sentiment_confidence'].mean() if 'sentiment_confidence' in theme_df.columns else 0
            }
        
        return correlations 