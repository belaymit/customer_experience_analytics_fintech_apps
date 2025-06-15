import pandas as pd
from pymongo import MongoClient
import logging
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MongoDBStorage:
    """Class to handle MongoDB Atlas storage operations"""
    
    def __init__(self, connection_string=None, database_name=None, collection_name=None):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string (str): MongoDB Atlas connection string
            database_name (str): Name of the database
            collection_name (str): Name of the collection
        """
        # Use environment variables or defaults
        self.connection_string = connection_string or os.getenv('MONGODB_URI')
        self.database_name = database_name or os.getenv('MONGODB_DATABASE', 'customer_reviews')
        self.collection_name = collection_name or os.getenv('MONGODB_COLLECTION', 'reviews')
        
        if not self.connection_string:
            raise ValueError("MongoDB URI must be provided in config.env file or as MONGODB_URI environment variable")
        
        self.client = None
        self.db = None
        self.collection = None
        
    def get_connection_string(self):
        """Get MongoDB connection string from environment or user input"""
        if self.connection_string:
            return self.connection_string
            
        # Get from user input as fallback
        print("\n" + "="*60)
        print("MONGODB ATLAS SETUP")
        print("="*60)
        print("MongoDB URI not found in environment variables.")
        print("Please set MONGODB_URI in config.env file or provide it now.")
        print("\nConnection string format:")
        print("mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority")
        print("\n" + "="*60)
        
        connection_string = input("Enter your MongoDB Atlas connection string: ").strip()
        
        if not connection_string:
            raise ValueError("MongoDB connection string is required")
            
        return connection_string
    
    def connect(self):
        """Establish connection to MongoDB Atlas"""
        try:
            self.connection_string = self.get_connection_string()
            
            logger.info("Connecting to MongoDB Atlas...")
            self.client = MongoClient(self.connection_string)
            
            # Test the connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB Atlas!")
            
            # Get database and collection
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            
            logger.info(f"Using database: {self.database_name}")
            logger.info(f"Using collection: {self.collection_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            return False
    
    def load_data(self, csv_file='data/cleaned_reviews.csv'):
        """Load cleaned data from CSV file"""
        try:
            logger.info(f"Loading data from {csv_file}")
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(df)} reviews")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None
    
    def prepare_documents(self, df):
        """Convert DataFrame to MongoDB documents"""
        logger.info("Preparing documents for MongoDB...")
        
        documents = []
        for _, row in df.iterrows():
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
                    'app_name': row.get('app_name', ''),
                    'data_version': '1.0',
                    'task': 'task_1_data_collection'
                }
            }
            documents.append(doc)
        
        logger.info(f"Prepared {len(documents)} documents")
        return documents
    
    def create_indexes(self):
        """Create indexes for better query performance"""
        try:
            logger.info("Creating database indexes...")
            
            # Create indexes for common query patterns
            indexes = [
                ('bank_name', 1),
                ('rating', 1),
                ('review_date', 1),
                ('uploaded_at', 1),
                [('bank_name', 1), ('rating', 1)],  # Compound index
                [('review_date', 1), ('bank_name', 1)]  # Compound index
            ]
            
            for index in indexes:
                try:
                    self.collection.create_index(index)
                    logger.info(f"Created index: {index}")
                except Exception as e:
                    logger.warning(f"Index creation failed for {index}: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {str(e)}")
    
    def insert_data(self, documents, batch_size=100):
        """Insert documents into MongoDB with batch processing"""
        try:
            logger.info(f"Inserting {len(documents)} documents...")
            
            # Check if collection already has data
            existing_count = self.collection.count_documents({})
            if existing_count > 0:
                logger.warning(f"Collection already contains {existing_count} documents")
                response = input("Do you want to clear existing data? (y/N): ").strip().lower()
                if response == 'y':
                    self.collection.delete_many({})
                    logger.info("Cleared existing data")
                else:
                    logger.info("Appending to existing data")
            
            # Insert in batches
            inserted_count = 0
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                try:
                    result = self.collection.insert_many(batch)
                    inserted_count += len(result.inserted_ids)
                    logger.info(f"Inserted batch {i//batch_size + 1}: {len(result.inserted_ids)} documents")
                except Exception as e:
                    logger.error(f"Error inserting batch {i//batch_size + 1}: {str(e)}")
            
            logger.info(f"✅ Successfully inserted {inserted_count} documents")
            return inserted_count
            
        except Exception as e:
            logger.error(f"Error inserting data: {str(e)}")
            return 0
    
    def verify_data(self):
        """Verify the uploaded data"""
        try:
            logger.info("Verifying uploaded data...")
            
            # Basic counts
            total_count = self.collection.count_documents({})
            logger.info(f"Total documents in collection: {total_count}")
            
            # Count by bank
            pipeline = [
                {"$group": {"_id": "$bank_name", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            bank_counts = list(self.collection.aggregate(pipeline))
            
            logger.info("Documents per bank:")
            for bank in bank_counts:
                logger.info(f"  {bank['_id']}: {bank['count']} reviews")
            
            # Rating distribution
            pipeline = [
                {"$group": {"_id": "$rating", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]
            rating_counts = list(self.collection.aggregate(pipeline))
            
            logger.info("Rating distribution:")
            for rating in rating_counts:
                logger.info(f"  {rating['_id']} stars: {rating['count']} reviews")
            
            # Sample document
            sample = self.collection.find_one()
            logger.info(f"Sample document structure: {list(sample.keys())}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error verifying data: {str(e)}")
            return False
    
    def generate_connection_info(self):
        """Generate connection information for future use"""
        info = {
            'database_name': self.database_name,
            'collection_name': self.collection_name,
            'total_documents': self.collection.count_documents({}),
            'last_updated': datetime.now().isoformat(),
            'connection_notes': {
                'driver': 'pymongo',
                'python_connection': f"MongoClient('{self.connection_string}')",
                'database_access': f"client['{self.database_name}']",
                'collection_access': f"db['{self.collection_name}']"
            }
        }
        
        # Save connection info
        with open('data/mongodb_connection_info.json', 'w') as f:
            # Remove sensitive connection string for security
            safe_info = info.copy()
            safe_info['connection_string_format'] = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority"
            json.dump(safe_info, f, indent=2)
        
        logger.info("Connection info saved to ../data/mongodb_connection_info.json")
        return info
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    def upload_complete_pipeline(self, csv_file='data/cleaned_reviews.csv'):
        """Complete pipeline to upload data to MongoDB"""
        logger.info("="*60)
        logger.info("STARTING MONGODB UPLOAD PIPELINE")
        logger.info("="*60)
        
        try:
            # Step 1: Connect to MongoDB
            if not self.connect():
                return False
            
            # Step 2: Load data
            df = self.load_data(csv_file)
            if df is None:
                return False
            
            # Step 3: Prepare documents
            documents = self.prepare_documents(df)
            
            # Step 4: Create indexes
            self.create_indexes()
            
            # Step 5: Insert data
            inserted_count = self.insert_data(documents)
            
            if inserted_count == 0:
                return False
            
            # Step 6: Verify data
            self.verify_data()
            
            # Step 7: Generate connection info
            self.generate_connection_info()
            
            logger.info("="*60)
            logger.info("✅ MONGODB UPLOAD COMPLETED SUCCESSFULLY!")
            logger.info("="*60)
            logger.info(f"📊 Uploaded {inserted_count} reviews to MongoDB Atlas")
            logger.info(f"🗄️  Database: {self.database_name}")
            logger.info(f"📁 Collection: {self.collection_name}")
            logger.info("🔗 Connection info saved for future use")
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return False
        finally:
            self.close_connection()

def main():
    """Main function to run MongoDB upload"""
    print("MongoDB Atlas Upload Tool")
    print("This tool will upload your cleaned review data to MongoDB Atlas")
    
    # Initialize storage handler
    storage = MongoDBStorage()
    
    # Run the complete pipeline
    success = storage.upload_complete_pipeline()
    
    if success:
        print("\nData successfully uploaded to MongoDB Atlas!")
        print("You can now use this data for analysis, Task 2, and beyond.")
    else:
        print("\nUpload failed. Please check the logs and try again.")

if __name__ == "__main__":
    main() 