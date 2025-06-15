#!/usr/bin/env python3
"""
Test script for Task 2 implementation
"""

import sys
import os

def test_imports():
    """Test if all required libraries can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        print("✓ pandas")
    except ImportError as e:
        print(f"✗ pandas: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy")
    except ImportError as e:
        print(f"✗ numpy: {e}")
        return False
    
    try:
        import nltk
        print("✓ nltk")
    except ImportError as e:
        print(f"✗ nltk: {e}")
        return False
    
    try:
        from textblob import TextBlob
        print("✓ textblob")
    except ImportError as e:
        print(f"✗ textblob: {e}")
        return False
    
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        print("✓ scikit-learn")
    except ImportError as e:
        print(f"✗ scikit-learn: {e}")
        return False
    
    try:
        from transformers import pipeline
        print("✓ transformers")
    except ImportError as e:
        print(f"⚠ transformers: {e} (will use TextBlob fallback)")
    
    return True

def test_data_availability():
    """Test if the required data files exist."""
    print("\n📁 Testing data availability...")
    
    required_files = [
        "data/cleaned_reviews.csv"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - File not found")
            return False
    
    return True

def test_analyzer():
    """Test the SentimentThematicAnalyzer class."""
    print("\n🔬 Testing analyzer initialization...")
    
    try:
        from task2_sentiment_analysis import SentimentThematicAnalyzer
        analyzer = SentimentThematicAnalyzer()
        print("✓ Analyzer initialized successfully")
        
        # Test preprocessing
        test_text = "This app is really slow and crashes frequently!"
        processed = analyzer.preprocess_text(test_text)
        print(f"✓ Text preprocessing: '{test_text}' -> '{processed}'")
        
        # Test sentiment analysis on a small sample
        test_texts = [
            "I love this app, it's amazing!",
            "This app is terrible and crashes all the time",
            "The app is okay, nothing special"
        ]
        
        results = analyzer.analyze_sentiment(test_texts)
        print("✓ Sentiment analysis test:")
        for i, (text, result) in enumerate(zip(test_texts, results)):
            print(f"  {i+1}. '{text}' -> {result['sentiment_label']} ({result['sentiment_score']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"✗ Analyzer test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running Task 2 Tests")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    # Test data availability
    if not test_data_availability():
        print("\n❌ Data availability tests failed. Please ensure data files exist.")
        return False
    
    # Test analyzer
    if not test_analyzer():
        print("\n❌ Analyzer tests failed.")
        return False
    
    print("\n✅ All tests passed! Ready to run Task 2 analysis.")
    print("\nTo run the full analysis, execute:")
    print("python task2_sentiment_analysis.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 