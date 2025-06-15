"""
Visualization utilities for sentiment and theme analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import logging
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

class SentimentVisualizer:
    """Handles visualization for sentiment and theme analysis."""
    
    def __init__(self, style: str = 'seaborn-v0_8', figsize: Tuple[int, int] = (12, 8)):
        self.logger = logging.getLogger(__name__)
        self.figsize = figsize
        
        # Set style
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        # Set color palette
        self.colors = {
            'positive': '#2E8B57',  # Sea Green
            'negative': '#DC143C',  # Crimson
            'neutral': '#4682B4',   # Steel Blue
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'tertiary': '#2ca02c'
        }
        
        # Set seaborn palette
        sns.set_palette("husl")
    
    def plot_sentiment_distribution(self, df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot sentiment distribution.
        
        Args:
            df (pd.DataFrame): Dataframe with sentiment analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        if 'sentiment_sentiment' in df.columns:
            # Pie chart
            sentiment_counts = df['sentiment_sentiment'].value_counts()
            colors = [self.colors.get(sentiment, '#gray') for sentiment in sentiment_counts.index]
            
            ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90)
            ax1.set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
            
            # Bar chart
            ax2.bar(sentiment_counts.index, sentiment_counts.values, color=colors)
            ax2.set_title('Sentiment Counts', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Sentiment')
            ax2.set_ylabel('Count')
            
            # Add value labels on bars
            for i, v in enumerate(sentiment_counts.values):
                ax2.text(i, v + 0.01 * max(sentiment_counts.values), str(v), 
                        ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_bank_sentiment_comparison(self, df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot sentiment comparison across banks.
        
        Args:
            df (pd.DataFrame): Dataframe with sentiment analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        if 'bank' not in df.columns or 'sentiment_sentiment' not in df.columns:
            return plt.figure()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Stacked bar chart
        sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_sentiment'], normalize='index') * 100
        sentiment_by_bank.plot(kind='bar', stacked=True, ax=ax1, 
                              color=[self.colors.get(col, '#gray') for col in sentiment_by_bank.columns])
        ax1.set_title('Sentiment Distribution by Bank (%)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Bank')
        ax1.set_ylabel('Percentage')
        ax1.legend(title='Sentiment')
        ax1.tick_params(axis='x', rotation=45)
        
        # Grouped bar chart
        sentiment_counts = pd.crosstab(df['bank'], df['sentiment_sentiment'])
        sentiment_counts.plot(kind='bar', ax=ax2, 
                             color=[self.colors.get(col, '#gray') for col in sentiment_counts.columns])
        ax2.set_title('Sentiment Counts by Bank', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Bank')
        ax2.set_ylabel('Count')
        ax2.legend(title='Sentiment')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_rating_sentiment_correlation(self, df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot correlation between ratings and sentiment.
        
        Args:
            df (pd.DataFrame): Dataframe with rating and sentiment data
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        if 'rating' not in df.columns or 'sentiment_sentiment' not in df.columns:
            return plt.figure()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Box plot
        sns.boxplot(data=df, x='sentiment_sentiment', y='rating', ax=ax1)
        ax1.set_title('Rating Distribution by Sentiment', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Sentiment')
        ax1.set_ylabel('Rating')
        
        # Heatmap
        rating_sentiment = pd.crosstab(df['rating'], df['sentiment_sentiment'], normalize='index')
        sns.heatmap(rating_sentiment, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax2)
        ax2.set_title('Rating vs Sentiment Heatmap', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Sentiment')
        ax2.set_ylabel('Rating')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_theme_distribution(self, df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot theme distribution.
        
        Args:
            df (pd.DataFrame): Dataframe with theme analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        theme_columns = [col for col in df.columns if col.startswith('theme_')]
        if not theme_columns:
            return plt.figure()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], self.figsize[1] * 1.2))
        
        # Theme counts
        theme_counts = {}
        for col in theme_columns:
            theme_name = col.replace('theme_', '').replace('_', ' ')
            theme_counts[theme_name] = df[col].sum()
        
        # Sort by count
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        themes, counts = zip(*sorted_themes)
        
        # Bar plot
        bars = ax1.bar(range(len(themes)), counts, color=plt.cm.Set3(np.linspace(0, 1, len(themes))))
        ax1.set_title('Theme Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Themes')
        ax1.set_ylabel('Count')
        ax1.set_xticks(range(len(themes)))
        ax1.set_xticklabels(themes, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01 * max(counts),
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        # Theme percentages
        total_reviews = len(df)
        theme_percentages = [count / total_reviews * 100 for count in counts]
        
        bars2 = ax2.bar(range(len(themes)), theme_percentages, color=plt.cm.Set3(np.linspace(0, 1, len(themes))))
        ax2.set_title('Theme Distribution (%)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Themes')
        ax2.set_ylabel('Percentage of Reviews')
        ax2.set_xticks(range(len(themes)))
        ax2.set_xticklabels(themes, rotation=45, ha='right')
        
        # Add percentage labels on bars
        for bar, pct in zip(bars2, theme_percentages):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01 * max(theme_percentages),
                    f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_theme_sentiment_heatmap(self, df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot heatmap of theme-sentiment correlations.
        
        Args:
            df (pd.DataFrame): Dataframe with theme and sentiment analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        theme_columns = [col for col in df.columns if col.startswith('theme_')]
        if not theme_columns or 'sentiment_sentiment' not in df.columns:
            return plt.figure()
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create correlation matrix
        correlation_data = []
        theme_names = []
        
        for col in theme_columns:
            theme_name = col.replace('theme_', '').replace('_', ' ')
            theme_names.append(theme_name)
            
            theme_df = df[df[col] == 1]
            if len(theme_df) > 0:
                sentiment_dist = theme_df['sentiment_sentiment'].value_counts(normalize=True)
                correlation_data.append([
                    sentiment_dist.get('positive', 0),
                    sentiment_dist.get('neutral', 0),
                    sentiment_dist.get('negative', 0)
                ])
            else:
                correlation_data.append([0, 0, 0])
        
        correlation_matrix = pd.DataFrame(
            correlation_data,
            index=theme_names,
            columns=['Positive', 'Neutral', 'Negative']
        )
        
        # Create heatmap
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='RdYlBu_r', 
                   center=0.33, ax=ax, cbar_kws={'label': 'Proportion'})
        ax.set_title('Theme-Sentiment Correlation Heatmap', fontsize=14, fontweight='bold')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Themes')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_wordcloud(self, texts: List[str], title: str = "Word Cloud", 
                        save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a word cloud from texts.
        
        Args:
            texts (List[str]): List of texts to create word cloud from
            title (str): Title for the word cloud
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        try:
            # Combine all texts
            combined_text = ' '.join(texts)
            
            # Create word cloud
            wordcloud = WordCloud(
                width=800, height=400,
                background_color='white',
                max_words=100,
                colormap='viridis'
            ).generate(combined_text)
            
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(title, fontsize=16, fontweight='bold')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Failed to create word cloud: {str(e)}")
            return plt.figure()
    
    def plot_sentiment_confidence_distribution(self, df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot distribution of sentiment confidence scores.
        
        Args:
            df (pd.DataFrame): Dataframe with sentiment confidence scores
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        if 'sentiment_confidence' not in df.columns:
            return plt.figure()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Histogram
        ax1.hist(df['sentiment_confidence'], bins=30, alpha=0.7, color=self.colors['primary'])
        ax1.set_title('Sentiment Confidence Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Confidence Score')
        ax1.set_ylabel('Frequency')
        ax1.axvline(df['sentiment_confidence'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["sentiment_confidence"].mean():.3f}')
        ax1.legend()
        
        # Box plot by sentiment
        if 'sentiment_sentiment' in df.columns:
            sns.boxplot(data=df, x='sentiment_sentiment', y='sentiment_confidence', ax=ax2)
            ax2.set_title('Confidence by Sentiment Type', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Sentiment')
            ax2.set_ylabel('Confidence Score')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_comprehensive_dashboard(self, df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a comprehensive dashboard with multiple visualizations.
        
        Args:
            df (pd.DataFrame): Dataframe with complete analysis results
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: The created figure
        """
        fig = plt.figure(figsize=(20, 16))
        
        # Create subplots
        gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)
        
        # 1. Sentiment Distribution
        ax1 = fig.add_subplot(gs[0, 0])
        if 'sentiment_sentiment' in df.columns:
            sentiment_counts = df['sentiment_sentiment'].value_counts()
            colors = [self.colors.get(sentiment, '#gray') for sentiment in sentiment_counts.index]
            ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90)
            ax1.set_title('Sentiment Distribution', fontweight='bold')
        
        # 2. Bank Comparison
        ax2 = fig.add_subplot(gs[0, 1])
        if 'bank' in df.columns and 'sentiment_sentiment' in df.columns:
            sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_sentiment'], normalize='index') * 100
            sentiment_by_bank.plot(kind='bar', stacked=True, ax=ax2, 
                                  color=[self.colors.get(col, '#gray') for col in sentiment_by_bank.columns])
            ax2.set_title('Sentiment by Bank (%)', fontweight='bold')
            ax2.tick_params(axis='x', rotation=45)
            ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 3. Rating Distribution
        ax3 = fig.add_subplot(gs[0, 2])
        if 'rating' in df.columns:
            df['rating'].hist(bins=5, ax=ax3, color=self.colors['secondary'], alpha=0.7)
            ax3.set_title('Rating Distribution', fontweight='bold')
            ax3.set_xlabel('Rating')
            ax3.set_ylabel('Frequency')
        
        # 4. Theme Distribution
        ax4 = fig.add_subplot(gs[1, :])
        theme_columns = [col for col in df.columns if col.startswith('theme_')]
        if theme_columns:
            theme_counts = {}
            for col in theme_columns:
                theme_name = col.replace('theme_', '').replace('_', ' ')
                theme_counts[theme_name] = df[col].sum()
            
            sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
            themes, counts = zip(*sorted_themes)
            
            bars = ax4.bar(range(len(themes)), counts, color=plt.cm.Set3(np.linspace(0, 1, len(themes))))
            ax4.set_title('Theme Distribution', fontweight='bold')
            ax4.set_xticks(range(len(themes)))
            ax4.set_xticklabels(themes, rotation=45, ha='right')
            ax4.set_ylabel('Count')
        
        # 5. Sentiment-Rating Correlation
        ax5 = fig.add_subplot(gs[2, 0])
        if 'rating' in df.columns and 'sentiment_sentiment' in df.columns:
            sns.boxplot(data=df, x='sentiment_sentiment', y='rating', ax=ax5)
            ax5.set_title('Rating by Sentiment', fontweight='bold')
        
        # 6. Confidence Distribution
        ax6 = fig.add_subplot(gs[2, 1])
        if 'sentiment_confidence' in df.columns:
            ax6.hist(df['sentiment_confidence'], bins=20, alpha=0.7, color=self.colors['tertiary'])
            ax6.set_title('Confidence Distribution', fontweight='bold')
            ax6.set_xlabel('Confidence Score')
        
        # 7. Review Length Distribution
        ax7 = fig.add_subplot(gs[2, 2])
        if 'review_length' in df.columns:
            ax7.hist(df['review_length'], bins=30, alpha=0.7, color=self.colors['primary'])
            ax7.set_title('Review Length Distribution', fontweight='bold')
            ax7.set_xlabel('Review Length (characters)')
        
        # 8. Theme-Sentiment Heatmap
        ax8 = fig.add_subplot(gs[3, :])
        if theme_columns and 'sentiment_sentiment' in df.columns:
            correlation_data = []
            theme_names = []
            
            for col in theme_columns[:8]:  # Limit to top 8 themes for readability
                theme_name = col.replace('theme_', '').replace('_', ' ')
                theme_names.append(theme_name)
                
                theme_df = df[df[col] == 1]
                if len(theme_df) > 0:
                    sentiment_dist = theme_df['sentiment_sentiment'].value_counts(normalize=True)
                    correlation_data.append([
                        sentiment_dist.get('positive', 0),
                        sentiment_dist.get('neutral', 0),
                        sentiment_dist.get('negative', 0)
                    ])
                else:
                    correlation_data.append([0, 0, 0])
            
            if correlation_data:
                correlation_matrix = pd.DataFrame(
                    correlation_data,
                    index=theme_names,
                    columns=['Positive', 'Neutral', 'Negative']
                )
                
                sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='RdYlBu_r', 
                           center=0.33, ax=ax8)
                ax8.set_title('Theme-Sentiment Correlation', fontweight='bold')
        
        plt.suptitle('Banking App Reviews - Sentiment & Theme Analysis Dashboard', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig