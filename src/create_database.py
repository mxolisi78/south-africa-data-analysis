"""
Database Creation Script for South Africa Data
===============================================

This script creates a SQLite database to store the processed data
for querying and analysis.

Inputs:
    - data/processed/south_africa_combined.csv

Outputs:
    - database/south_africa_data.db

Author: Your Name
Date: 2026-08-28
"""

import sqlite3
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define directories (following your structure)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
DB_DIR = BASE_DIR / "database"

# Create database directory if it doesn't exist
DB_DIR.mkdir(parents=True, exist_ok=True)


def create_database():
    """
    Create SQLite database and populate with data.
    """
    logger.info("=" * 60)
    logger.info("CREATING DATABASE")
    logger.info("=" * 60)
    
    # Database file path
    db_path = DB_DIR / "south_africa_data.db"
    logger.info(f"Database path: {db_path}")
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Load the processed data
    logger.info("Loading processed data...")
    data_path = DATA_DIR / "south_africa_combined.csv"
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} observations")
    
    # Create table
    logger.info("Creating table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS south_africa_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            unemployment_rate REAL,
            tertiary_enrolment REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert data
    logger.info("Inserting data...")
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO south_africa_data 
            (year, unemployment_rate, tertiary_enrolment)
            VALUES (?, ?, ?)
        ''', (
            int(row['Year']),
            float(row['Unemployment_Rate']),
            float(row['Tertiary_Enrolment'])
        ))
    
    # Commit changes
    conn.commit()
    logger.info(f"Inserted {len(df)} records")
    
    # Create indexes for faster queries
    logger.info("Creating indexes...")
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_year ON south_africa_data(year)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_unemployment ON south_africa_data(unemployment_rate)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_enrolment ON south_africa_data(tertiary_enrolment)')
    
    # Get record count
    cursor.execute("SELECT COUNT(*) FROM south_africa_data")
    count = cursor.fetchone()[0]
    logger.info(f"Total records: {count}")
    
    # Show sample data
    cursor.execute("SELECT * FROM south_africa_data LIMIT 5")
    sample = cursor.fetchall()
    logger.info("Sample data:")
    for row in sample:
        logger.info(f"  {row}")
    
    # Close connection
    conn.close()
    
    logger.info(f"✅ Database created at: {db_path}")
    
    return db_path


def query_database():
    """
    Demonstrate querying the database.
    """
    logger.info("\n" + "=" * 60)
    logger.info("QUERYING THE DATABASE")
    logger.info("=" * 60)
    
    db_path = DB_DIR / "south_africa_data.db"
    conn = sqlite3.connect(db_path)
    
    # Example queries
    queries = [
        ("1. All data (first 5 rows)", 
         "SELECT * FROM south_africa_data ORDER BY year LIMIT 5"),
        ("2. Data from 2000 onwards", 
         "SELECT year, unemployment_rate, tertiary_enrolment FROM south_africa_data WHERE year >= 2000 ORDER BY year"),
        ("3. Highest unemployment years (top 5)", 
         "SELECT year, unemployment_rate FROM south_africa_data ORDER BY unemployment_rate DESC LIMIT 5"),
        ("4. Highest enrolment years (top 5)", 
         "SELECT year, tertiary_enrolment FROM south_africa_data ORDER BY tertiary_enrolment DESC LIMIT 5"),
        ("5. Summary statistics", 
         """
         SELECT 
             COUNT(*) as total_records,
             MIN(year) as min_year,
             MAX(year) as max_year,
             ROUND(AVG(unemployment_rate), 2) as avg_unemployment,
             ROUND(MIN(unemployment_rate), 2) as min_unemployment,
             ROUND(MAX(unemployment_rate), 2) as max_unemployment,
             ROUND(AVG(tertiary_enrolment), 2) as avg_enrolment,
             ROUND(MIN(tertiary_enrolment), 2) as min_enrolment,
             ROUND(MAX(tertiary_enrolment), 2) as max_enrolment
         FROM south_africa_data
         """),
        ("6. Years with unemployment > 30%", 
         "SELECT year, unemployment_rate FROM south_africa_data WHERE unemployment_rate > 30 ORDER BY year"),
        ("7. Years with enrolment > 20%", 
         "SELECT year, tertiary_enrolment FROM south_africa_data WHERE tertiary_enrolment > 20 ORDER BY year"),
        ("8. Year-over-year changes", 
         """
         SELECT 
             year,
             unemployment_rate,
             tertiary_enrolment,
             LAG(unemployment_rate) OVER (ORDER BY year) as prev_unemployment,
             ROUND(unemployment_rate - LAG(unemployment_rate) OVER (ORDER BY year), 2) as unemployment_change
         FROM south_africa_data
         ORDER BY year
         """)
    ]
    
    for title, query in queries:
        logger.info(f"\n{title}")
        logger.info("-" * 40)
        try:
            result = pd.read_sql_query(query, conn)
            print(result)
        except Exception as e:
            logger.error(f"Query failed: {e}")
    
    conn.close()


def export_from_database():
    """
    Export data from database to CSV in the database folder.
    """
    logger.info("\n" + "=" * 60)
    logger.info("EXPORTING FROM DATABASE")
    logger.info("=" * 60)
    
    db_path = DB_DIR / "south_africa_data.db"
    conn = sqlite3.connect(db_path)
    
    # Export full dataset
    df = pd.read_sql_query("SELECT * FROM south_africa_data ORDER BY year", conn)
    
    # Save to CSV in database folder
    export_path = DB_DIR / "south_africa_data_export.csv"
    df.to_csv(export_path, index=False)
    logger.info(f"Exported {len(df)} records to: {export_path}")
    
    # Export summary statistics
    summary = pd.read_sql_query("""
        SELECT 
            COUNT(*) as total_records,
            MIN(year) as min_year,
            MAX(year) as max_year,
            ROUND(AVG(unemployment_rate), 2) as avg_unemployment,
            ROUND(MIN(unemployment_rate), 2) as min_unemployment,
            ROUND(MAX(unemployment_rate), 2) as max_unemployment,
            ROUND(AVG(tertiary_enrolment), 2) as avg_enrolment,
            ROUND(MIN(tertiary_enrolment), 2) as min_enrolment,
            ROUND(MAX(tertiary_enrolment), 2) as max_enrolment
        FROM south_africa_data
    """, conn)
    
    summary_path = DB_DIR / "database_summary.csv"
    summary.to_csv(summary_path, index=False)
    logger.info(f"Summary exported to: {summary_path}")
    
    conn.close()


def main():
    """Main execution function."""
    # Create database
    db_path = create_database()
    
    # Query database
    query_database()
    
    # Export from database
    export_from_database()
    
    logger.info("\n" + "=" * 60)
    logger.info("DATABASE OPERATIONS COMPLETED SUCCESSFULLY")
    logger.info("=" * 60)
    logger.info(f"Database: {db_path}")
    logger.info(f"Database directory: {DB_DIR}")
    
    # List files in database directory
    logger.info("\nFiles in database directory:")
    for file in DB_DIR.iterdir():
        logger.info(f"  - {file.name}")


if __name__ == "__main__":
    main()