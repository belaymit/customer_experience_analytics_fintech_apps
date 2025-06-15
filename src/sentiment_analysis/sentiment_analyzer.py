"""
Sentiment analysis module using DistilBERT and TextBlob.
"""

import pandas as pd
from typing import Dict, List
import logging
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class SentimentAnalyzer:
    """Handles sentiment analysis using DistilBERT and TextBlob."""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.sentiment_pipeline = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the sentiment analysis model."""
        if TRANSFORMERS_AVAILABLE:
            try:
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=self.model_name,
                    return_all_scores=True
                )
                self.logger.info(f"Initialized DistilBERT model: {self.model_name}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize DistilBERT: {str(e)}")
                self.sentiment_pipeline = None
        else:
            self.logger.warning("Transformers not available, using TextBlob only")
    
    def analyze_sentiment_distilbert(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using DistilBERT.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, float]: Sentiment scores
        """
        if not self.sentiment_pipeline:
            return self.analyze_sentiment_textblob(text)
        
        try:
            # Truncate text if too long (DistilBERT has token limits)
            if len(text) > 512:
                text = text[:512]
            
            results = self.sentiment_pipeline(text)[0]
            
            # Convert to standardized format
            sentiment_scores = {}
            for result in results:
                label = result['label'].lower()
                score = result['score']
                
                if label == 'positive':
                    sentiment_scores['positive'] = score
                elif label == 'negative':
                    sentiment_scores['negative'] = score
                else:
                    sentiment_scores[label] = score
            
            # Calculate neutral score if not present
            if 'neutral' not in sentiment_scores:
                sentiment_scores['neutral'] = 1.0 - sum(sentiment_scores.values())
            
            # Determine overall sentiment
            max_sentiment = max(sentiment_scores.items(), key=lambda x: x[1])
            sentiment_scores['sentiment'] = max_sentiment[0]
            sentiment_scores['confidence'] = max_sentiment[1]
            
            return sentiment_scores
            
        except Exception as e:
            self.logger.warning(f"DistilBERT analysis failed: {str(e)}, falling back to TextBlob")
            return self.analyze_sentiment_textblob(text)
    
    def analyze_sentiment_textblob(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using TextBlob.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, float]: Sentiment scores
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Convert polarity to positive/negative/neutral scores
            if polarity > 0.1:
                sentiment = 'positive'
                positive_score = (polarity + 1) / 2
                negative_score = 1 - positive_score
                neutral_score = 0.1
            elif polarity < -0.1:
                sentiment = 'negative'
                negative_score = abs(polarity - 1) / 2
                positive_score = 1 - negative_score
                neutral_score = 0.1
            else:
                sentiment = 'neutral'
                neutral_score = 0.8
                positive_score = 0.1
                negative_score = 0.1
            
            return {
                'positive': positive_score,
                'negative': negative_score,
                'neutral': neutral_score,
                'sentiment': sentiment,
                'confidence': max(positive_score, negative_score, neutral_score),
                'polarity': polarity,
                'subjectivity': subjectivity
            }
            
        except Exception as e:
            self.logger.error(f"TextBlob analysis failed: {str(e)}")
            return {
                'positive': 0.33,
                'negative': 0.33,
                'neutral': 0.34,
                'sentiment': 'neutral',
                'confidence': 0.34,
                'polarity': 0.0,
                'subjectivity': 0.0
            }
    
    def analyze_batch(self, texts: List[str], use_distilbert: bool = True) -> List[Dict[str, float]]:
        """
        Analyze sentiment for a batch of texts.
        
        Args:
            texts (List[str]): List of texts to analyze
            use_distilbert (bool): Whether to use DistilBERT (falls back to TextBlob)
            
        Returns:
            List[Dict[str, float]]: List of sentiment analysis results
        """
        results = []
        
        for i, text in enumerate(texts):
            if i % 100 == 0:
                self.logger.info(f"Processing text {i+1}/{len(texts)}")
            
            if use_distilbert and self.sentiment_pipeline:
                result = self.analyze_sentiment_distilbert(text)
            else:
                result = self.analyze_sentiment_textblob(text)
            
            results.append(result)
        
        return results
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'review') -> pd.DataFrame:
        """
        Analyze sentiment for all texts in a dataframe.
        
        Args:
            df (pd.DataFrame): Dataframe containing texts
            text_column (str): Name of the text column
            
        Returns:
            pd.DataFrame: Dataframe with sentiment analysis results
        """
        df_result = df.copy()
        
        # Analyze sentiments
        texts = df_result[text_column].astype(str).tolist()
        sentiment_results = self.analyze_batch(texts)
        
        # Add results to dataframe
        for key in ['positive', 'negative', 'neutral', 'sentiment', 'confidence']:
            df_result[f'sentiment_{key}'] = [result.get(key, 0) for result in sentiment_results]
        
        # Add polarity and subjectivity if available (from TextBlob)
        if 'polarity' in sentiment_results[0]:
            df_result['sentiment_polarity'] = [result.get('polarity', 0) for result in sentiment_results]
            df_result['sentiment_subjectivity'] = [result.get('subjectivity', 0) for result in sentiment_results]
        
        return df_result
    
    def get_sentiment_summary(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Get summary statistics of sentiment analysis.
        
        Args:
            df (pd.DataFrame): Dataframe with sentiment analysis results
            
        Returns:
            Dict[str, any]: Summary statistics
        """
        if 'sentiment_sentiment' not in df.columns:
            return {}
        
        sentiment_counts = df['sentiment_sentiment'].value_counts()
        total_reviews = len(df)
        
        summary = {
            'total_reviews': total_reviews,
            'sentiment_distribution': {
                'positive': sentiment_counts.get('positive', 0),
                'negative': sentiment_counts.get('negative', 0),
                'neutral': sentiment_counts.get('neutral', 0)
            },
            'sentiment_percentages': {
                'positive': (sentiment_counts.get('positive', 0) / total_reviews) * 100,
                'negative': (sentiment_counts.get('negative', 0) / total_reviews) * 100,
                'neutral': (sentiment_counts.get('neutral', 0) / total_reviews) * 100
            },
            'average_confidence': df['sentiment_confidence'].mean() if 'sentiment_confidence' in df.columns else 0,
            'average_scores': {
                'positive': df['sentiment_positive'].mean() if 'sentiment_positive' in df.columns else 0,
                'negative': df['sentiment_negative'].mean() if 'sentiment_negative' in df.columns else 0,
                'neutral': df['sentiment_neutral'].mean() if 'sentiment_neutral' in df.columns else 0
            }
        }
        
        # Add polarity stats if available
        if 'sentiment_polarity' in df.columns:
            summary['polarity_stats'] = {
                'mean': df['sentiment_polarity'].mean(),
                'std': df['sentiment_polarity'].std(),
                'min': df['sentiment_polarity'].min(),
                'max': df['sentiment_polarity'].max()
            }
        
        return summary 