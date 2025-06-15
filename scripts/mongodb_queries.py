from pymongo import MongoClient
import logging
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MongoDBAnalyzer:
    """Class for analyzing bank review data in MongoDB"""
    
    def __init__(self, connection_string=None, database_name=None, collection_name=None):
        # Use environment variables or defaults
        self.connection_string = connection_string or os.getenv('MONGODB_URI')
        self.database_name = database_name or os.getenv('MONGODB_DATABASE', 'customer_reviews')
        self.collection_name = collection_name or os.getenv('MONGODB_COLLECTION', 'reviews')
        
        if not self.connection_string:
            raise ValueError("MongoDB URI must be provided in config.env file or as MONGODB_URI environment variable")
        
        self.client = None
        self.db = None
        self.collection = None
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            logger.info("Connected to MongoDB Atlas")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            return False
    
    def basic_statistics(self):
        """Get basic statistics about the data"""
        logger.info("=== BASIC STATISTICS ===")
        
        # Total count
        total = self.collection.count_documents({})
        logger.info(f"Total reviews: {total}")
        
        # Count by bank
        pipeline = [
            {"$group": {"_id": "$bank_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        bank_stats = list(self.collection.aggregate(pipeline))
        logger.info("Reviews per bank:")
        for stat in bank_stats:
            logger.info(f"  {stat['_id']}: {stat['count']}")
        
        # Rating distribution
        pipeline = [
            {"$group": {"_id": "$rating", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        rating_stats = list(self.collection.aggregate(pipeline))
        logger.info("Rating distribution:")
        for stat in rating_stats:
            logger.info(f"  {stat['_id']} stars: {stat['count']}")
    
    def sentiment_analysis_prep(self):
        """Prepare data for sentiment analysis (Task 2)"""
        logger.info("=== SENTIMENT ANALYSIS PREPARATION ===")
        
        # Get reviews by rating (proxy for sentiment)
        positive_reviews = self.collection.find({"rating": {"$gte": 4}}).limit(5)
        negative_reviews = self.collection.find({"rating": {"$lte": 2}}).limit(5)
        
        logger.info("Sample positive reviews (4-5 stars):")
        for i, review in enumerate(positive_reviews, 1):
            logger.info(f"  {i}. [{review['bank_name']}] {review['review_text'][:100]}...")
        
        logger.info("Sample negative reviews (1-2 stars):")
        for i, review in enumerate(negative_reviews, 1):
            logger.info(f"  {i}. [{review['bank_name']}] {review['review_text'][:100]}...")
    
    def bank_comparison(self):
        """Compare banks by various metrics"""
        logger.info("=== BANK COMPARISON ===")
        
        # Average rating by bank
        pipeline = [
            {"$group": {
                "_id": "$bank_name",
                "avg_rating": {"$avg": "$rating"},
                "total_reviews": {"$sum": 1},
                "avg_review_length": {"$avg": "$review_length"}
            }},
            {"$sort": {"avg_rating": -1}}
        ]
        
        bank_comparison = list(self.collection.aggregate(pipeline))
        logger.info("Bank comparison:")
        for bank in bank_comparison:
            logger.info(f"  {bank['_id']}:")
            logger.info(f"    Average rating: {bank['avg_rating']:.2f}")
            logger.info(f"    Total reviews: {bank['total_reviews']}")
            logger.info(f"    Avg review length: {bank['avg_review_length']:.1f} chars")
    
    def temporal_analysis(self):
        """Analyze reviews over time"""
        logger.info("=== TEMPORAL ANALYSIS ===")
        
        # Reviews by year
        pipeline = [
            {"$addFields": {
                "year": {"$year": {"$dateFromString": {"dateString": "$review_date"}}}
            }},
            {"$group": {
                "_id": "$year",
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        
        yearly_stats = list(self.collection.aggregate(pipeline))
        logger.info("Reviews by year:")
        for stat in yearly_stats:
            logger.info(f"  {stat['_id']}: {stat['count']} reviews")
    
    def keyword_extraction_prep(self):
        """Prepare data for keyword extraction"""
        logger.info("=== KEYWORD EXTRACTION PREPARATION ===")
        
        # Get reviews with specific keywords
        keywords = ["crash", "slow", "fast", "good", "bad", "bug", "error"]
        
        for keyword in keywords:
            count = self.collection.count_documents({
                "review_text": {"$regex": keyword, "$options": "i"}
            })
            logger.info(f"Reviews containing '{keyword}': {count}")
    
    def export_for_analysis(self, output_file="../data/mongodb_export.json"):
        """Export data for external analysis"""
        logger.info("=== EXPORTING DATA ===")
        
        # Export all reviews
        reviews = list(self.collection.find({}, {"_id": 0}))
        
        with open(output_file, 'w') as f:
            json.dump(reviews, f, indent=2, default=str)
        
        logger.info(f"Exported {len(reviews)} reviews to {output_file}")
    
    def advanced_aggregations(self):
        """Advanced aggregation examples"""
        logger.info("=== ADVANCED AGGREGATIONS ===")
        
        # Rating distribution by bank
        pipeline = [
            {"$group": {
                "_id": {
                    "bank": "$bank_name",
                    "rating": "$rating"
                },
                "count": {"$sum": 1}
            }},
            {"$group": {
                "_id": "$_id.bank",
                "ratings": {
                    "$push": {
                        "rating": "$_id.rating",
                        "count": "$count"
                    }
                }
            }},
            {"$sort": {"_id": 1}}
        ]
        
        rating_by_bank = list(self.collection.aggregate(pipeline))
        logger.info("Rating distribution by bank:")
        for bank in rating_by_bank:
            logger.info(f"  {bank['_id']}:")
            for rating in sorted(bank['ratings'], key=lambda x: x['rating']):
                logger.info(f"    {rating['rating']} stars: {rating['count']} reviews")
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()
            logger.info("Connection closed")

def main():
    """Main function to run analysis examples"""
    print("MongoDB Analysis Examples")
    print("This script demonstrates various queries for analyzing bank review data")
    print("Using MongoDB configuration from config.env file")
    print()
    
    try:
        # Initialize analyzer with environment variables
        analyzer = MongoDBAnalyzer()
        
        if not analyzer.connect():
            print("Failed to connect to MongoDB")
            return
        
        print("Connected to MongoDB Atlas successfully!")
        print(f"Database: {analyzer.database_name}")
        print(f"Collection: {analyzer.collection_name}")
        print("="*60)
        
        # Run various analyses
        analyzer.basic_statistics()
        print()
        analyzer.bank_comparison()
        print()
        analyzer.sentiment_analysis_prep()
        print()
        analyzer.temporal_analysis()
        print()
        analyzer.keyword_extraction_prep()
        print()
        analyzer.advanced_aggregations()
        print()
        analyzer.export_for_analysis("data/mongodb_export.json")
        
        print("\n" + "="*60)
        print("Analysis complete! Check data/mongodb_export.json for exported data.")
        print("Your MongoDB Atlas database is ready for Task 2 (Sentiment Analysis)!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        print(f"\nAnalysis failed: {str(e)}")
        print("Please check your config.env file and MongoDB connection.")
    finally:
        if 'analyzer' in locals():
            analyzer.close()

if __name__ == "__main__":
    main() 