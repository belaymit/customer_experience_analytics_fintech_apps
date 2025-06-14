# MongoDB Atlas Setup Guide

This guide will help you set up MongoDB Atlas (cloud database) to store your bank review data.

## Prerequisites

- MongoDB Atlas account (free tier available)
- Python environment with pymongo installed

## Step 1: Create MongoDB Atlas Account

1. **Sign up for MongoDB Atlas**:
   - Go to [https://www.mongodb.com/atlas](https://www.mongodb.com/atlas)
   - Click "Try Free" and create an account
   - Choose the **FREE** tier (M0 Sandbox)

2. **Create a Cluster**:
   - Select a cloud provider (AWS, Google Cloud, or Azure)
   - Choose a region close to your location
   - Keep the default cluster name or choose your own
   - Click "Create Cluster" (this may take a few minutes)

## Step 2: Configure Database Access

1. **Create Database User**:
   - Go to "Database Access" in the left sidebar
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Create a username and strong password
   - Set privileges to "Read and write to any database"
   - Click "Add User"

2. **Configure Network Access**:
   - Go to "Network Access" in the left sidebar
   - Click "Add IP Address"
   - For development, you can click "Allow Access from Anywhere" (0.0.0.0/0)
   - For production, add only your specific IP address
   - Click "Confirm"

## Step 3: Get Connection String

1. **Get Connection String**:
   - Go to "Clusters" in the left sidebar
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Select "Python" and version "3.6 or later"
   - Copy the connection string

2. **Connection String Format**:
   ```
   mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/<database-name>?retryWrites=true&w=majority
   ```

3. **Replace Placeholders**:
   - `<username>`: Your database username
   - `<password>`: Your database password
   - `<cluster-name>`: Your cluster name
   - `<database-name>`: Use `bank_reviews_db`

## Step 4: Upload Your Data

### Option 1: Using the Upload Script

1. **Run the MongoDB upload script**:
   ```bash
   cd scripts
   python mongodb_storage.py
   ```

2. **Enter your connection string** when prompted

3. **The script will**:
   - Connect to your MongoDB Atlas cluster
   - Create the database and collection
   - Upload all 1,137 reviews
   - Create indexes for better performance
   - Verify the upload

### Option 2: Manual Configuration

If you prefer to set up environment variables:

1. **Create a `.env` file** (in project root):
   ```bash
   MONGODB_URI=your_connection_string_here
   MONGODB_DATABASE=bank_reviews_db
   MONGODB_COLLECTION=reviews
   ```

2. **Run the script**:
   ```bash
   python mongodb_storage.py
   ```

## Step 5: Verify Your Data

### Using MongoDB Atlas Web Interface

1. **Browse Collections**:
   - Go to "Clusters" → "Browse Collections"
   - You should see `bank_reviews_db` database
   - Click on `reviews` collection
   - Browse your uploaded documents

### Using the Query Script

1. **Run analysis queries**:
   ```bash
   python mongodb_queries.py
   ```

2. **This will show**:
   - Basic statistics
   - Bank comparisons
   - Sample queries for analysis

## Database Schema

Your data will be stored with this structure:

```json
{
  "review_id": "CBE_1",
  "review_text": "The app is great but sometimes slow...",
  "rating": 4,
  "review_date": "2025-06-13",
  "bank_name": "CBE",
  "source": "Google Play Store",
  "review_length": 156,
  "word_count": 28,
  "processed_at": "2025-06-14 10:42:45",
  "uploaded_at": "2025-06-14T10:45:30.123456",
  "metadata": {
    "app_name": "Commercial Bank of Ethiopia",
    "data_version": "1.0",
    "task": "task_1_data_collection"
  }
}
```

## Useful MongoDB Queries

### Basic Queries

```python
# Count total reviews
db.reviews.count_documents({})

# Find reviews by bank
db.reviews.find({"bank_name": "CBE"})

# Find high-rated reviews
db.reviews.find({"rating": {"$gte": 4}})

# Find recent reviews
db.reviews.find({"review_date": {"$gte": "2025-01-01"}})
```

### Aggregation Examples

```python
# Average rating by bank
db.reviews.aggregate([
    {"$group": {
        "_id": "$bank_name",
        "avg_rating": {"$avg": "$rating"},
        "count": {"$sum": 1}
    }}
])

# Rating distribution
db.reviews.aggregate([
    {"$group": {
        "_id": "$rating",
        "count": {"$sum": 1}
    }},
    {"$sort": {"_id": 1}}
])
```

## Next Steps

1. **Task 2 Integration**: Use MongoDB data for sentiment analysis
2. **Advanced Queries**: Explore the `mongodb_queries.py` script
3. **Visualization**: Connect to BI tools like MongoDB Charts
4. **Backup**: Set up automated backups in Atlas

## Troubleshooting

### Common Issues

1. **Connection Timeout**:
   - Check your network access settings
   - Verify your IP is whitelisted

2. **Authentication Failed**:
   - Double-check username and password
   - Ensure user has proper permissions

3. **Database Not Found**:
   - The database will be created automatically on first insert
   - Check your connection string format

### Getting Help

- MongoDB Atlas Documentation: [https://docs.atlas.mongodb.com/](https://docs.atlas.mongodb.com/)
- MongoDB University (Free Courses): [https://university.mongodb.com/](https://university.mongodb.com/)
- Community Forums: [https://community.mongodb.com/](https://community.mongodb.com/)

## Security Best Practices

1. **Use Strong Passwords**: For database users
2. **Limit Network Access**: Only allow necessary IP addresses
3. **Regular Backups**: Enable automated backups
4. **Monitor Access**: Review database access logs
5. **Environment Variables**: Never commit connection strings to git

---

**🎉 Congratulations!** Your bank review data is now stored in MongoDB Atlas and ready for advanced analysis! 