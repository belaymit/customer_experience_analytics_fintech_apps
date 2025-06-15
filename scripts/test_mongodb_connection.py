from pymongo import MongoClient
import pandas as pd
import logging
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MongoDBTester:
    """Class to test MongoDB Atlas connection and operations"""
    
    def __init__(self):
        # Use environment variables
        self.connection_string = os.getenv('MONGODB_URI')
        self.database_name = os.getenv('MONGODB_DATABASE', 'customer_reviews')
        self.collection_name = os.getenv('MONGODB_COLLECTION', 'reviews')
        
        if not self.connection_string:
            raise ValueError("MongoDB URI must be provided in config.env file or as MONGODB_URI environment variable")
        
        # Extract cluster info for logging
        if '@' in self.connection_string:
            self.cluster = self.connection_string.split('@')[1].split('/')[0].split('?')[0]
        else:
            self.cluster = "MongoDB Atlas"
        
        self.client = None
        self.db = None
        self.collection = None
    
    def test_connection(self):
        """Test the MongoDB Atlas connection"""
        try:
            logger.info("Testing MongoDB Atlas connection...")
            logger.info(f"Connecting to cluster: {self.cluster}")
            logger.info(f"Database: {self.database_name}")
            logger.info(f"Collection: {self.collection_name}")
            
            # Create client
            self.client = MongoClient(self.connection_string)
            
            # Test the connection with ping
            self.client.admin.command('ping')
            logger.info("✅ Successfully connected to MongoDB Atlas!")
            
            # Get database and collection
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            
            # Test database access
            db_list = self.client.list_database_names()
            logger.info(f"Available databases: {db_list}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Connection failed: {str(e)}")
            return False
    
    def test_write_operation(self):
        """Test writing data to MongoDB"""
        try:
            logger.info("Testing write operation...")
            
            # Create a test document
            test_doc = {
                "review_id": "TEST_001",
                "review_text": "This is a test review for MongoDB connection",
                "rating": 5,
                "review_date": "2025-06-14",
                "bank_name": "TEST_BANK",
                "source": "Test Source",
                "review_length": 45,
                "word_count": 9,
                "processed_at": datetime.now().isoformat(),
                "uploaded_at": datetime.now().isoformat(),
                "metadata": {
                    "test": True,
                    "data_version": "1.0",
                    "task": "connection_test"
                }
            }
            
            # Insert the test document
            result = self.collection.insert_one(test_doc)
            logger.info(f"✅ Test document inserted with ID: {result.inserted_id}")
            
            return result.inserted_id
            
        except Exception as e:
            logger.error(f"❌ Write operation failed: {str(e)}")
            return None
    
    def test_read_operation(self, doc_id):
        """Test reading data from MongoDB"""
        try:
            logger.info("Testing read operation...")
            
            # Find the test document
            doc = self.collection.find_one({"_id": doc_id})
            
            if doc:
                logger.info("✅ Successfully retrieved test document:")
                logger.info(f"   Review ID: {doc['review_id']}")
                logger.info(f"   Review Text: {doc['review_text']}")
                logger.info(f"   Rating: {doc['rating']}")
                logger.info(f"   Bank: {doc['bank_name']}")
                return True
            else:
                logger.error("❌ Could not retrieve test document")
                return False
                
        except Exception as e:
            logger.error(f"❌ Read operation failed: {str(e)}")
            return False
    
    def test_query_operations(self):
        """Test various query operations"""
        try:
            logger.info("Testing query operations...")
            
            # Count documents
            total_docs = self.collection.count_documents({})
            logger.info(f"Total documents in collection: {total_docs}")
            
            # Find test documents
            test_docs = self.collection.count_documents({"metadata.test": True})
            logger.info(f"Test documents found: {test_docs}")
            
            # Test aggregation
            pipeline = [
                {"$group": {"_id": "$bank_name", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            
            bank_counts = list(self.collection.aggregate(pipeline))
            logger.info("Documents by bank:")
            for bank in bank_counts:
                logger.info(f"   {bank['_id']}: {bank['count']} documents")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Query operations failed: {str(e)}")
            return False
    
    def upload_sample_data(self):
        """Upload a small sample of the actual review data"""
        try:
            logger.info("Uploading sample review data...")
            
            # Load a few rows from the cleaned data
            df = pd.read_csv('data/cleaned_reviews.csv')
            sample_df = df.head(5)  # Just 5 reviews for testing
            
            documents = []
            for _, row in sample_df.iterrows():
                doc = {
                    'review_id': f"{row['bank']}_{len(documents) + 1}",
                    'review_text': row['review'],
                    'rating': int(row['rating']),
                    'review_date': row['date'],
                    'bank_name': row['bank'],
                    'source': row['source'],
                    'review_length': int(row['review_length']),
                    'word_count': int(row['word_count']),
                    'processed_at': row['processed_at'],
                    'uploaded_at': datetime.now().isoformat(),
                    'metadata': {
                        'data_version': '1.0',
                        'task': 'sample_upload_test',
                        'sample': True
                    }
                }
                documents.append(doc)
            
            # Insert the documents
            result = self.collection.insert_many(documents)
            logger.info(f"✅ Uploaded {len(result.inserted_ids)} sample reviews")
            
            return len(result.inserted_ids)
            
        except Exception as e:
            logger.error(f"❌ Sample data upload failed: {str(e)}")
            return 0
    
    def cleanup_test_data(self):
        """Clean up test data"""
        try:
            logger.info("Cleaning up test data...")
            
            # Remove test documents
            result = self.collection.delete_many({"metadata.test": True})
            logger.info(f"Deleted {result.deleted_count} test documents")
            
            # Remove sample documents
            result = self.collection.delete_many({"metadata.sample": True})
            logger.info(f"Deleted {result.deleted_count} sample documents")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {str(e)}")
            return False
    
    def close_connection(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    def run_complete_test(self):
        """Run the complete test suite"""
        logger.info("="*60)
        logger.info("MONGODB ATLAS CONNECTION TEST")
        logger.info("="*60)
        logger.info(f"Testing connection to: {self.cluster}")
        logger.info(f"Database: {self.database_name}")
        logger.info(f"Collection: {self.collection_name}")
        logger.info("="*60)
        
        try:
            # Test 1: Connection
            if not self.test_connection():
                return False
            
            # Test 2: Write operation
            doc_id = self.test_write_operation()
            if not doc_id:
                return False
            
            # Test 3: Read operation
            if not self.test_read_operation(doc_id):
                return False
            
            # Test 4: Query operations
            if not self.test_query_operations():
                return False
            
            # Test 5: Upload sample data
            uploaded_count = self.upload_sample_data()
            if uploaded_count == 0:
                return False
            
            # Test 6: Final verification
            total_docs = self.collection.count_documents({})
            logger.info(f"Final document count: {total_docs}")
            
            # Test 7: Cleanup
            self.cleanup_test_data()
            
            logger.info("="*60)
            logger.info("✅ ALL TESTS PASSED!")
            logger.info("✅ MongoDB Atlas is ready for your data!")
            logger.info("="*60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Test suite failed: {str(e)}")
            return False
        finally:
            self.close_connection()

def main():
    """Main function to run the MongoDB test"""
    print("MongoDB Atlas Connection Tester")
    print("This will test your MongoDB Atlas connection and basic operations")
    print()
    
    tester = MongoDBTester()
    success = tester.run_complete_test()
    
    if success:
        print("\nMongoDB Atlas is working perfectly!")
        print("You can now upload your full dataset using mongodb_storage.py")
    else:
        print("\nMongoDB Atlas test failed!")
        print("Please check your connection string and database configuration")

if __name__ == "__main__":
    main() 