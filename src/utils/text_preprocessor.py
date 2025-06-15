"""
Text preprocessing utilities for sentiment analysis.
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from typing import List, Optional
import logging

class TextPreprocessor:
    """Handles advanced text preprocessing for sentiment analysis."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.lemmatizer = WordNetLemmatizer()
        self._setup_nltk()
        
    def _setup_nltk(self):
        """Download required NLTK data."""
        nltk_downloads = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']
        for item in nltk_downloads:
            try:
                nltk.data.find(f'tokenizers/{item}')
            except LookupError:
                try:
                    nltk.download(item, quiet=True)
                except:
                    self.logger.warning(f"Could not download {item}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text (str): Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text (str): Text to tokenize
            
        Returns:
            List[str]: List of tokens
        """
        try:
            tokens = word_tokenize(text)
            return tokens
        except:
            # Fallback to simple split if NLTK fails
            return text.split()
    
    def remove_stopwords(self, tokens: List[str], language: str = 'english') -> List[str]:
        """
        Remove stopwords from tokens.
        
        Args:
            tokens (List[str]): List of tokens
            language (str): Language for stopwords
            
        Returns:
            List[str]: Tokens without stopwords
        """
        try:
            stop_words = set(stopwords.words(language))
            return [token for token in tokens if token.lower() not in stop_words]
        except:
            # Fallback stopwords if NLTK fails
            basic_stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
            return [token for token in tokens if token.lower() not in basic_stopwords]
    
    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens.
        
        Args:
            tokens (List[str]): List of tokens
            
        Returns:
            List[str]: Lemmatized tokens
        """
        try:
            return [self.lemmatizer.lemmatize(token) for token in tokens]
        except:
            # Return original tokens if lemmatization fails
            return tokens
    
    def preprocess_text(self, text: str, remove_stopwords: bool = True, lemmatize: bool = True) -> str:
        """
        Complete text preprocessing pipeline.
        
        Args:
            text (str): Raw text to preprocess
            remove_stopwords (bool): Whether to remove stopwords
            lemmatize (bool): Whether to lemmatize tokens
            
        Returns:
            str: Preprocessed text
        """
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize_text(cleaned_text)
        
        # Remove stopwords
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        if lemmatize:
            tokens = self.lemmatize_tokens(tokens)
        
        # Filter out empty tokens and very short words
        tokens = [token for token in tokens if len(token) > 2]
        
        return ' '.join(tokens)
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract keywords from text using simple frequency analysis.
        
        Args:
            text (str): Text to extract keywords from
            top_n (int): Number of top keywords to return
            
        Returns:
            List[str]: List of keywords
        """
        processed_text = self.preprocess_text(text)
        tokens = processed_text.split()
        
        # Count frequency
        word_freq = {}
        for token in tokens:
            word_freq[token] = word_freq.get(token, 0) + 1
        
        # Sort by frequency and return top N
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]] 